# RSI focused literature-search report

Search date: 2026-09-14. Queries: `robot self-improvement` and `robot recursive self-improvement`; window 2024–2026; max 3 per query per source. Six API sources searched concurrently; source read timeout 40 seconds, two attempts. Retrieval is intentionally bounded, not a comprehensive survey.

per-source hits: arxiv=0, dblp=0, open_alex=6, openreview=0, semantic_scholar=0, crossref=6

unique papers: 10 (2 cross-source duplicate records merged); no relevance filter applied.

## All ranked unique hits (unaltered order)

| # | Title | Year / date returned | Venue returned | Citations | Score | Sources |
|---|---|---|---|---:|---:|---|
| [1](https://doi.org/10.48550/arxiv.2505.01396) | SIME: Enhancing Policy Self-Improvement with Modal-level Exploration | 2025 | arXiv (Cornell University) | 0 | 3 | OpenAlex |
| [2](https://doi.org/10.1109/aris62416.2024.10680004) | Design and Control Algorithm Improvement for Modular Self-Reconfigurable Robot | 2024 | 2024 International Conference on Advanced Robotics and Intelligent Systems (ARIS) | 0 | 3 | Crossref |
| [3](https://doi.org/10.2139/ssrn.6091646) | Authority Transfer in Recursive and Networked AI Systems Closed-Loop Self-Improvement (CLSI), Recursive Leverage (RLF), and Synchronized Recursive Leverage (SRL) | Unknown | Not supplied | 0 | 3 | Crossref |
| [4](https://doi.org/10.2139/ssrn.6082447) | On Closed-Loop Self-Improvement Interval (CLSI) and Recursive Leverage Factor (RLF) A Conceptual Framework for Recursive Intelligence Systems | Unknown | Not supplied | 0 | 3 | Crossref |
| [5](https://doi.org/10.2139/ssrn.5841962) | Human Superintelligence: How you can develop it using recursive self-improvement | Unknown | Not supplied | 0 | 3 | Crossref |
| [6](https://doi.org/10.70777/si.v2i3.15063) | Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents | 2025 | SuperIntelligence - Robotics - Safety & Alignment | 18 | 2 | OpenAlex |
| [7](https://doi.org/10.1109/icra57147.2024.10610485) | Grow Your Limits: Continuous Improvement with Real-World RL for Robotic Locomotion | 2024 | Not supplied (DOI is ICRA) | 12 | 2 | OpenAlex |
| [8](https://doi.org/10.3233/faia251129) | Training Robotic Self-Evolving with GRPO | 2025 | Frontiers in artificial intelligence and applications | 0 | 2 | OpenAlex |
| [9](https://doi.org/10.47191/etj/v11i05.54) | Improvement, Upgrade, and Development of Robots for The "Robot 2025 – Winning Faith" Competition | 2026 | Engineering and Technology Journal | 0 | 2 | Crossref |
| [10](https://doi.org/10.55092/rl20250006) | Combination of decision making and machine learning for improvement of robot learning for water analysis | 2025 | Robot Learning | 0 | 2 | Crossref |

arXiv, DBLP, OpenReview and Semantic Scholar returned 0, with failures below. OpenAlex and Crossref are the only successful API surfaces; the result set has substantial off-topic contamination. Unknown-year hits are retained exactly as returned, not silently treated as in-window. The venue/DOI for [6] was not adopted as canonical: independently located original paper is [arXiv:2505.22954](https://arxiv.org/html/2505.22954v1) and [Sakana project article](https://sakana.ai/dgm/).

### Model Knowledge (0 additional unverified entries)

No model-memory-only papers are added. Known lineage mentioned in the main note is supported by primary source retrieval rather than recalled titles. Do not pad this set with speculative 2026 titles.

## Summary of all searched results

### 1. Overview

The queries yielded 10 unique hits, mostly broad self-improvement or unrelated robotics applications. The newest relevant ENPIRE, ASPIRE and RoboRSI were recovered through first-party GitHub/project/arXiv links, not this unreliable keyword result set. API failures mean this retrieval cannot establish absence of additional work.

### 2. Trends

This tiny error-affected sample cannot establish temporal or venue trends. Its 2024 hits include ordinary robot-control engineering and real-world RL, while a 2025 hit concerns self-modifying coding agents. The 2026 primary sources followed separately show agent-driven robot research/skill accumulation, but that observation should not be presented as a bibliometric trend inferred from these 10 records.

### 3. Key themes

- Policy improvement and RL: [1], [7], [8]; not necessarily agent-driven or recursive.
- Self-modifying software agents and conceptual recursion: [3], [4], [6]; robotic capability is not demonstrated by their titles.
- Conventional robot-engineering use of “improvement”: [2], [9], [10], illustrating lexical false positives.
- Human self-improvement: [5], out of scope despite lexical score.

### 4. Keywords frequency

Title-level binary counts, not stemming across unrelated meanings. Exact code-defined concept patterns below avoid assigning scientific relevance from keywords alone.

| Keyword / concept | Titles containing it |
|---|---:|
| Improvement / improving | 9 |
| Robot / robotic / robots | 5 |
| Self-improvement / self-improving | 5 |
| Recursive | 3 |
| Learning | 1 |

### 5. Most cited by accepted paper

Accepted status is not independently verified across this result set, so a top-five “accepted” ranking is not defensible. These are the only clearly conference-labelled/DOI-identifiable entries, with source-reported citation counts, not a global ranking.

| Rank | Title | Year | Citations |
|---|---|---:|---:|
| 1 | Grow Your Limits: Continuous Improvement with Real-World RL for Robotic Locomotion (ICRA DOI) | 2024 | 12 |
| 2 | Design and Control Algorithm Improvement for Modular Self-Reconfigurable Robot (ARIS venue) | 2024 | 0 |

### 6. Most cited by first author

Only these retrieval records contribute; counts may be incomplete and the DGM alternate bibliographic record is unaudited. Zero-citation ties ordered by occurrence; this is not a field-level ranking.

| Rank | Author | Papers in set | Total citations |
|---|---|---:|---:|
| 1 | Jenny Zhang | 1 | 18 |
| 2 | Laura Smith | 1 | 12 |
| 3 | Jin Yang | 1 | 0 |
| 4 | Po-Lin Li | 1 | 0 |
| 5 | Adrian Erckenbrack | 2 | 0 |

### 7. Recommendations for reading

1. [ENPIRE](https://arxiv.org/html/2606.19980v1): physical autoresearch via fixed environment contracts; primary anchor already in talk.
2. [ASPIRE](https://arxiv.org/html/2607.00272v1): persistent repair knowledge and held-out transfer; distinguish from weight updates.
3. [RoboRSI](https://lab.noematrix.ai/blog/2-roborsi/): September 2026 research report linking online exploration, code consolidation and a small policy-training case. Read original metric definitions rather than treating adaptive task coverage as frozen SR.

These three recommendations are primary sources followed after the broad retrieval, **not claimed to be hits in the ranked API table**. DGM [6] is optional conceptual background, not a fourth robot case study.

## Errors verbatim

```text
[arxiv] HTTP 429; retrying in 3s (attempt 2/2)
[arxiv] Error on query 'robot self-improvement': 429 Client Error: Unknown Error for url: https://export.arxiv.org/api/query?search_query=%28all%3Arobot+self-improvement%29+AND+submittedDate%3A%5B202401010000+TO+202612312359%5D&sortBy=relevance&sortOrder=descending&max_results=3
[arxiv] Error on query 'robot recursive self-improvement': HTTPSConnectionPool(host='export.arxiv.org', port=443): Max retries exceeded with url: /api/query?search_query=%28all%3Arobot+recursive+self-improvement%29+AND+submittedDate%3A%5B202401010000+TO+202612312359%5D&sortBy=relevance&sortOrder=descending&max_results=3 (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1000)')))
[dblp] Error on query 'robot self-improvement': Expecting value: line 1 column 1 (char 0)
[dblp] Error on query 'robot recursive self-improvement': Expecting value: line 1 column 1 (char 0)
[open_alex] HTTP 504; retrying in 3s (attempt 2/2)
[openreview] Error on query 'robot self-improvement': openreview not installed. pip install openreview-py
[openreview] Error on query 'robot recursive self-improvement': openreview not installed. pip install openreview-py
[semantic_scholar] HTTP 429; retrying in 3s (attempt 2/2)
[semantic_scholar] Error on query 'robot self-improvement': 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/search?query=robot+self-improvement&offset=0&limit=3&fields=title%2Cauthors%2Cyear%2Cabstract%2CcitationCount%2Curl%2Cvenue%2CpublicationDate%2CexternalIds&year=2024-2026
[semantic_scholar] HTTP 429; retrying in 3s (attempt 2/2)
[semantic_scholar] Error on query 'robot recursive self-improvement': 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/search?query=robot+recursive+self-improvement&offset=0&limit=3&fields=title%2Cauthors%2Cyear%2Cabstract%2CcitationCount%2Curl%2Cvenue%2CpublicationDate%2CexternalIds&year=2024-2026
```

The OpenReview error is a missing connector dependency, not a claim that public OpenReview records require credentials. No dependencies or model runtimes were installed for this read-only research.

## Additional discovery boundaries

- GitHub unauthenticated repository search found `NVlabs/ENPIRE`, `NVlabs/ASPIRE`, `nssmd/RoboRSI` and `lixuan27/roborise`; query result JSON snapshots live one directory above.
- RoboRISE was a title-only placeholder at inspected revision; no results claimed.
- Google plain-HTML fetch returned client-challenge markup. Bing returned unrelated search records (finance / consumer sites) despite topical query text; these were retained as failed low-signal discovery snapshots and not used for conclusions.
- Direct NVIDIA project-page fetches failed with `SSL: UNEXPECTED_EOF_WHILE_READING`; existing full paper snapshots and fresh official GitHub code remained readable.
- Fresh arXiv abstract checks confirm ENPIRE and ASPIRE currently expose only v1; the saved full paper snapshots remain the versioned source.
