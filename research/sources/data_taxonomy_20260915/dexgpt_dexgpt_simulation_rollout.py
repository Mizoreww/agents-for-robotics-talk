"""Contact-only physics replay, compared with explicitly kinematic reconstruction."""
from dexgpt.paths import ROOT, OUT
import json
import cv2
import imageio.v2 as imageio
import mujoco
import numpy as np
from PIL import Image
from dexgpt.motion.retarget import hand_ids


def initialize(m,d,track):
    for s,side in enumerate(['right','left']):
        _,qa,_,_=hand_ids(m,side)
        ra=m.joint(side+'_root').qposadr[0]
        d.qpos[ra:ra+7]=track['roots'][0,s]
        mocap=m.body(side+'_target').mocapid[0]
        d.mocap_pos[mocap]=track['roots'][0,s,:3]
        d.mocap_quat[mocap]=track['roots'][0,s,3:]
        ids=[m.actuator(n).id for n in hand_ids(m,side)[0]]
        d.qpos[qa]=track['ctrl'][0,ids]
    d.ctrl[:]=track['ctrl'][0]
    d.joint('mixer_hinge').qpos[0]=track['hinge_reference'][0]
    mujoco.mj_forward(m,d)

def main(feedback=False):
    track=np.load(OUT/'retargeted.npz')
    m=mujoco.MjModel.from_xml_path(str(OUT/'scene.xml'))
    d=mujoco.MjData(m); reference=mujoco.MjData(m)
    initialize(m,d,track); initialize(m,reference,track)
    from scipy.spatial.transform import Rotation
    pivot=np.array([.077,0,.232])
    r0=track['roots'][0,0]
    inv=Rotation.from_rotvec([0,-track['hinge_reference'][0],0])
    local_wrist=inv.apply(r0[:3]-pivot)
    local_rot=inv*Rotation.from_quat(r0[[4,5,6,3]])
    n=len(track['time']); frame_dt=float(np.median(np.diff(track['time'])))
    clip=Image.open(ROOT/'human.gif')
    qa=np.array([m.joint(m.actuator(i).trnid[0]).qposadr[0] for i in range(m.nu)])
    rootqa=[m.joint(side+'_root').qposadr[0] for side in ['right','left']]
    mocaps=[m.body(side+'_target').mocapid[0] for side in ['right','left']]
    hand_bodies={i for i in range(m.nbody) if m.body(i).name.startswith(('right__','left__'))}
    object_geoms={m.geom(name).id for name in ['lever','blue_head','pink_knob','beater_shaft','beater','mixer_body','base_plate']}
    head_geoms={m.geom(name).id for name in ['lever','blue_head','pink_knob','beater_shaft','beater']}
    actual=[]; states=[]; velocities=[]; all_controls=[]; contact_counts=[]; penetration=[]; forces=[]
    frame_contact=0; frame_head_contact=0; frame_pen=0.; frame_force=0.
    head_counts=[]; torque_peak=np.zeros(m.nu)
    with mujoco.Renderer(m,height=480,width=640) as renderer, imageio.get_writer(OUT/'comparison.mp4',fps=1/frame_dt,macro_block_size=1) as video:
        for i in range(n):
            if i:
                steps=round(frame_dt/m.opt.timestep)
                for sub in range(steps):
                    fraction=(sub+1)/steps
                    d.ctrl[:]=(1-fraction)*track['ctrl'][i-1]+fraction*track['ctrl'][i]
                    for s in range(2):
                        pose=(1-fraction)*track['roots'][i-1,s]+fraction*track['roots'][i,s]
                        d.mocap_pos[mocaps[s]]=pose[:3]
                        d.mocap_quat[mocaps[s]]=pose[3:]/np.linalg.norm(pose[3:])
                    if feedback:
                        desired=(1-fraction)*track['hinge_reference'][i-1]+fraction*track['hinge_reference'][i]
                        measured=float(d.joint('mixer_hinge').qpos[0])
                        commanded=measured+np.clip(desired-measured,-.12,.12)
                        turn=Rotation.from_rotvec([0,commanded,0])
                        d.mocap_pos[mocaps[0]]=pivot+turn.apply(local_wrist)
                        d.mocap_quat[mocaps[0]]=(turn*local_rot).as_quat()[[3,0,1,2]]
                    mujoco.mj_step(m,d)
                    if not np.isfinite(d.qpos).all() or np.max(np.abs(d.qvel))>1e4:
                        raise RuntimeError(f'Unstable dynamics at frame {i}')
                    torque_peak=np.maximum(torque_peak,np.abs(d.actuator_force))
                    for contact_id,c in enumerate(d.contact):
                        g1,g2=int(c.geom1),int(c.geom2)
                        is_hand_object=((g1 in object_geoms and int(m.geom_bodyid[g2]) in hand_bodies) or
                                        (g2 in object_geoms and int(m.geom_bodyid[g1]) in hand_bodies))
                        if is_hand_object:
                            frame_contact+=1
                            frame_head_contact+=int(g1 in head_geoms or g2 in head_geoms)
                            frame_pen=max(frame_pen,-float(c.dist))
                            force=np.zeros(6); mujoco.mj_contactForce(m,d,contact_id,force)
                            frame_force=max(frame_force,float(np.linalg.norm(force[:3])))
            actual.append(float(d.joint('mixer_hinge').qpos[0]))
            states.append(d.qpos.copy()); velocities.append(d.qvel.copy()); all_controls.append(d.ctrl.copy())
            contact_counts.append(frame_contact); head_counts.append(frame_head_contact); penetration.append(frame_pen); forces.append(frame_force)
            frame_contact=frame_head_contact=0; frame_pen=frame_force=0.
            reference.qpos[qa]=track['ctrl'][i]
            reference.joint('mixer_hinge').qpos[0]=track['hinge_reference'][i]
            for s in range(2):
                reference.qpos[rootqa[s]:rootqa[s]+7]=track['roots'][i,s]
            mujoco.mj_forward(m,reference)
            renderer.update_scene(reference,camera='front'); ref_image=renderer.render().copy()
            renderer.update_scene(d,camera='front'); sim_image=renderer.render().copy()
            clip.seek(i); source=np.asarray(clip.convert('RGB')); source=cv2.resize(source,(640,440))
            source=cv2.copyMakeBorder(source,20,20,0,0,cv2.BORDER_CONSTANT,value=(20,25,32))
            canvas=np.zeros((540,1920,3),dtype=np.uint8);canvas[:]=[18,23,31]
            canvas[44:524,:640]=source;canvas[44:524,640:1280]=ref_image;canvas[44:524,1280:]=sim_image
            labels=['SOURCE | human.gif','KINEMATIC RECONSTRUCTION | imposed hinge','CONTACT PHYSICS | passive hinge']
            for j,label in enumerate(labels):
                cv2.putText(canvas,label,(j*640+16,28),cv2.FONT_HERSHEY_SIMPLEX,.57,(220,235,245),1,cv2.LINE_AA)
            label=f't={track["time"][i]:.1f}s   reference={np.rad2deg(track["hinge_reference"][i]):.1f} deg   physics={np.rad2deg(actual[-1]):.1f} deg'
            cv2.putText(canvas,label,(1294,510),cv2.FONT_HERSHEY_SIMPLEX,.44,(255,210,100),1,cv2.LINE_AA)
            video.append_data(canvas)
            if i in [0,34,68,102,136,170,202]:
                Image.fromarray(canvas).save(OUT/f'frame_{i:03d}.jpg')
            if i%40==0: print(f'Physics/render {i}/{n}',flush=True)
    actual=np.array(actual); error=actual-track['hinge_reference']
    rms=float(np.rad2deg(np.sqrt(np.mean(error**2))))
    max_pen=float(max(penetration)*1000)
    success=rms<10 and max_pen<5 and np.mean(np.array(head_counts)>0)>.3
    report={'frames':n,'simulated_seconds':float(d.time),'physics_timestep_seconds':m.opt.timestep,
            'hinge_rmse_degrees':rms,'hinge_reference_range_degrees':np.rad2deg([track['hinge_reference'].min(),track['hinge_reference'].max()]).tolist(),
            'hinge_physics_range_degrees':np.rad2deg([actual.min(),actual.max()]).tolist(),
            'frames_with_hand_object_contacts_fraction':float(np.mean(np.array(contact_counts)>0)),
            'frames_with_hand_head_contacts_fraction':float(np.mean(np.array(head_counts)>0)),
            'maximum_hand_object_penetration_mm':max_pen,'peak_hand_object_contact_force_N':float(max(forces)),
            'finite_states':bool(np.isfinite(states).all()),'mujoco_warning_counts':d.warning.number.tolist(),
            'task_success':bool(success),'success_criteria':'hinge RMSE <10 degrees, maximum penetration <5 mm, head contact in >30% of frames',
            'wrist_controller': 'hinge feedback with 0.12 rad lookahead' if feedback else 'open-loop trajectory',
            'object_actuation':'none: mixer hinge is passive; only wrist drives and 44 hand actuators are commanded',
            'limitations':['Uncalibrated scale/depth and primitive toy geometry','Toy base is fixed to table','Prescribed wrist trajectories stand in for robot arms','Kinematic reconstruction is not evidence of physical task success'],
            'peak_actuator_force':torque_peak.tolist()}
    np.savez_compressed(OUT/'physics_rollout.npz',time=track['time'],qpos=states,qvel=velocities,ctrl=all_controls,
                        hinge_actual=actual,hinge_reference=track['hinge_reference'],hand_object_contact_counts=contact_counts,
                        hand_head_contact_counts=head_counts,max_penetration_m=penetration,peak_contact_force_N=forces)
    (OUT/'physics_report.json').write_text(json.dumps(report,indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axs=plt.subplots(2,1,figsize=(10,6),sharex=True)
    axs[0].plot(track['time'],np.rad2deg(track['hinge_reference']),label='Video estimate')
    axs[0].plot(track['time'],np.rad2deg(actual),label='Passive hinge physics');axs[0].set_ylabel('Hinge angle (deg)');axs[0].legend()
    axs[1].plot(track['time'],np.array(penetration)*1000,label='Hand/object penetration')
    axs[1].set_ylabel('Penetration (mm)');axs[1].set_xlabel('Time (s)');axs[1].legend()
    fig.tight_layout();fig.savefig(OUT/'validation.png',dpi=160);plt.close(fig)
    print(json.dumps({k:v for k,v in report.items() if k!='peak_actuator_force'},indent=2),flush=True)

if __name__=='__main__':
    main()
