<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=220&section=header&text=Raj%20Vardhan%20Kumar&fontSize=44&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Backend%20%26%20Distributed%20Systems%20Engineer&descAlignY=55&descSize=18" width="100%"/>

<img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&pause=1000&color=A78BFA&center=true&vCenter=true&width=650&lines=Backend+%26+Distributed+Systems+Engineer;C%2B%2B+%7C+Full-Stack+Developer;Building+Self-Healing%2C+Fault-Tolerant+Systems;Competitive+Programmer+%7C+400%2B+DSA+Problems" alt="Typing SVG" />

<br/>

![B.Tech Geoinformatics](https://img.shields.io/badge/B.Tech-Geoinformatics-6D28D9?style=flat-square&labelColor=1a1a2e)
![University](https://img.shields.io/badge/NSUT-New%20Delhi-4C1D95?style=flat-square&labelColor=1a1a2e)
![Location](https://img.shields.io/badge/📍-New%20Delhi%2C%20India-312E81?style=flat-square&labelColor=1a1a2e)

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-6D28D9?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/rajvardhankumar)
[![Email](https://img.shields.io/badge/Email-5B21B6?style=for-the-badge&logo=gmail&logoColor=white)](mailto:raj.kumar.ug23@nsut.ac.in)
[![GitHub](https://img.shields.io/badge/GitHub-4C1D95?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rajvardhan-git-sys)

<br/>

![Profile Views](https://komarev.com/ghpvc/?username=rajvardhan-git-sys&color=7c3aed&style=flat-square&label=Profile+Views)
![Followers](https://img.shields.io/github/followers/rajvardhan-git-sys?color=6D28D9&style=flat-square&label=Followers)
![Stars](https://img.shields.io/github/stars/rajvardhan-git-sys?color=4C1D95&style=flat-square&label=Stars)

</div>

---

## 👋 About Me

I'm a Software Engineering undergraduate at **Netaji Subhas University of Technology (NSUT)**, New Delhi, focused on **backend engineering, distributed systems, and full-stack development**. I like building things that stay up under pressure — from a self-healing, consistent-hashing cache cluster in C++ to a real-time NGO platform serving 11 districts.

My work sits at the intersection of **systems programming** (concurrency, networking, fault tolerance) and **product engineering** (shipping full-stack applications people actually use). I care about correctness under load as much as I care about clean UX.

```yaml
open_to:
  - Software Engineering Internships (Backend / Systems)
  - Full-Stack Development Roles
  - Open Source Collaboration
  - Competitive Programming Teams
```

---

## 🛠️ Tech Stack

**Languages**

<img src="https://skillicons.dev/icons?i=cpp,js,html,css&theme=dark" />

**Frontend**

<img src="https://skillicons.dev/icons?i=html,css,js&theme=dark" />

**Backend & Databases**

<img src="https://skillicons.dev/icons?i=nodejs,postgres,mongodb&theme=dark" />

**Tooling & Infra**

<img src="https://skillicons.dev/icons?i=git,github,linux,cmake,vscode&theme=dark" />

> Also working with: Boost.Asio · POSIX Sockets · Supabase · REST APIs · Google reCAPTCHA v3

---

## 🧠 Core Engineering Expertise

<div align="center">

| Domain | Proficiency | Details |
|---|---|---|
| **Distributed Systems** | Intermediate–Advanced | Sharded/replicated caching, consistent hashing with virtual nodes, zero-downtime rebalancing |
| **Concurrent Programming** | Advanced | `std::thread`, `mutex`, `condition_variable`; heartbeat-based failure detection & automatic failover |
| **Networking** | Intermediate–Advanced | Boost.Asio async I/O, POSIX sockets, custom message header/body protocols |
| **Backend & Databases** | Intermediate | PostgreSQL schema design, 20+ indexes, Supabase, load-tested to 2,000+ req/s |
| **Full-Stack Web Development** | Intermediate | Full-stack platforms, GeoJSON-based interactive SVG maps, secure form handling |

</div>

---

## 🚀 Featured Projects

<details open>
<summary><b>🔄 Self-Healing Distributed Cache</b> — C++, POSIX Sockets, CMake</summary>
<br/>

Architected a sharded, replicated in-memory cache cluster designed to survive node failures without data loss or downtime, using consistent hashing with virtual nodes instead of naive modulo hashing.

| Aspect | Details |
|---|---|
| **Stack** | C++, POSIX Sockets, CMake, `std::thread` / `mutex` / `condition_variable` |
| **Scale** | Multi-node sharded, replicated cluster |
| **Performance** | Key remapping limited to under `[X]%` on node join/leave vs. full reshuffling under modulo hashing |
| **Reliability** | Sustained `[X]%` read availability when a primary node was killed mid-traffic |
| **Resilience** | Zero-downtime rebalancing + TTL-consistent replica sync; chaos-tested by force-killing random nodes under live load with 100% request success within one client-side retry |
| **Repository** | [github.com/rajvardhan-git-sys/self-healing-cache](https://github.com/rajvardhan-git-sys/self-healing-cache) |

Built heartbeat-based failure detection and automatic failover from scratch, then validated the whole system with a custom chaos-testing harness rather than trusting it by inspection.

</details>

<details>
<summary><b>💬 chatRoomCpp — Multi-Client Chat Room Application</b> — C++, Boost.Asio</summary>
<br/>

A multi-client chat server built on Boost.Asio's asynchronous, non-blocking I/O model, supporting several concurrent clients without blocking on any single connection.

| Aspect | Details |
|---|---|
| **Stack** | C++, Boost.Asio |
| **Architecture** | `Session`, `Room`, and `Message` classes to manage connections, routing, and encode/decode logic |
| **Concurrency** | Dedicated thread per client session for real-time, non-blocking chat |
| **Security** | Structured message header/body encoding to prevent malformed-frame issues |
| **Impact** | Reusable foundation for real-time multi-client networked applications |
| **Repository** | [github.com/rajvardhan-git-sys/chatRoomCpp](https://github.com/rajvardhan-git-sys/chatRoomCpp) |

</details>

<details>
<summary><b>🌍 AVBH Foundation — NGO Web Platform</b> — Full-Stack, Supabase (PostgreSQL)</summary>
<br/>

A full-stack platform delivering real-time beneficiary tracking for an NGO operating across 11 Delhi districts.

| Aspect | Details |
|---|---|
| **Stack** | Full-stack, Supabase (PostgreSQL), GeoJSON, Google reCAPTCHA v3 |
| **Scale** | 12-page platform, real-time tracking across 11 Delhi districts |
| **Performance** | Load-tested to sustain 2,000+ requests/second with zero errors |
| **Security** | 4 forms secured with Google reCAPTCHA v3 |
| **Impact** | Interactive GeoJSON-based SVG map with hover/click filtering and animated counters for beneficiary data |
| **Repository** | [github.com/rajvardhan-git-sys/avbh-platform](https://github.com/rajvardhan-git-sys/avbh-platform) |

</details>

---

## 💼 Experience

### AVBH Foundation — NGO Web Platform
**New Delhi, India** · *May 2026 – Aug 2026*

Architected and shipped a full-stack platform for an NGO tracking beneficiaries in real time across 11 Delhi districts.

- Built a 12-page full-stack application on a Supabase (PostgreSQL) backend
- Designed an interactive GeoJSON-based SVG map of Delhi districts with hover/click filtering and animated counters
- Secured 4 public-facing forms with Google reCAPTCHA v3
- Optimized the database with 20+ PostgreSQL indexes; load-tested to sustain 2,000+ requests/second with zero errors

<div align="center">

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4C1D95?style=flat-square&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-6D28D9?style=flat-square&logo=supabase&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-312E81?style=flat-square&logo=javascript&logoColor=white)
![GeoJSON](https://img.shields.io/badge/GeoJSON-5B21B6?style=flat-square&logo=mapbox&logoColor=white)

</div>

---

## 🏆 Achievements

<div align="center">

| Recognition | Details |
|---|---|
| 🧩 LeetCode | 400+ DSA problems solved — Graphs, Dynamic Programming, Trees |
| 🥈 CodeChef Round 1022 (Div. 2) | Global Rank **2693** out of 30,000+ participants |
| ⚡ Educational Codeforces Round 192 (Div. 2 Rated) | Global Rank **460** |

</div>

---

## 📜 Certifications

> No certifications were listed on the source resume — add your AWS / Oracle / NPTEL / Cisco badges here as you earn them.

---

## 💻 Coding Profiles

<div align="center">

[![LeetCode](https://img.shields.io/badge/LeetCode-6D28D9?style=for-the-badge&logo=leetcode&logoColor=white)](https://leetcode.com/Venompro)
[![Codeforces](https://img.shields.io/badge/Codeforces-4C1D95?style=for-the-badge&logo=codeforces&logoColor=white)](https://codeforces.com/profile/VenomMax)
[![CodeChef](https://img.shields.io/badge/CodeChef-5B21B6?style=for-the-badge&logo=codechef&logoColor=white)](https://www.codechef.com/users/YOUR_CODECHEF_USERNAME)
[![GeeksforGeeks](https://img.shields.io/badge/GeeksforGeeks-312E81?style=for-the-badge&logo=geeksforgeeks&logoColor=white)](https://auth.geeksforgeeks.org/user/YOUR_GFG_USERNAME)

</div>

---

## 📊 GitHub Analytics

<div align="center">

<img src="https://github-readme-stats.vercel.app/api?username=rajvardhan-git-sys&show_icons=true&theme=radical&hide_border=true&bg_color=0d0221&title_color=A78BFA&icon_color=7C3AED&text_color=c9d1d9" width="49%"/>
<img src="https://github-readme-streak-stats.herokuapp.com/?user=rajvardhan-git-sys&theme=radical&hide_border=true&background=0d0221&stroke=A78BFA&ring=7C3AED&fire=6D28D9" width="49%"/>

<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=rajvardhan-git-sys&layout=compact&theme=radical&hide_border=true&bg_color=0d0221&title_color=A78BFA&text_color=c9d1d9" width="45%"/>

</div>

---

## 🏅 GitHub Trophies

<div align="center">

<img src="https://github-profile-trophy.vercel.app/?username=rajvardhan-git-sys&theme=algolia&no-frame=true&margin-w=10&column=7" />

</div>

---

## 📈 Contribution Activity

<div align="center">

<img src="https://github-readme-activity-graph.vercel.app/graph?username=rajvardhan-git-sys&theme=react-dark&bg_color=0d0221&color=A78BFA&line=7C3AED&point=ffffff&hide_border=true" width="100%"/>

</div>

---

## 🐍 Contribution Snake

<div align="center">

<img src="https://raw.githubusercontent.com/rajvardhan-git-sys/rajvardhan-git-sys/output/github-contribution-grid-snake-dark.svg" width="100%"/>

<sub>Generated via <a href="https://github.com/Platane/snk">Platane/snk</a> — requires a GitHub Actions workflow on your profile repo.</sub>

</div>

---

## 🎯 Current Focus

```yaml
current_focus:
  learning:
    - System Design at scale
    - Advanced distributed systems patterns
  building:
    - Self-Healing Distributed Cache (C++)
    - Backend systems focused on fault tolerance
  exploring:
    - Cloud-native infrastructure
    - Kubernetes & containerized deployments
  open_to:
    - Software Engineering Internships
    - Backend / Systems Engineering roles
    - Open source collaboration
```

---

## 📬 Connect With Me

<div align="center">

[![Gmail](https://img.shields.io/badge/raj.kumar.ug23%40nsut.ac.in-6D28D9?style=for-the-badge&logo=gmail&logoColor=white)](mailto:raj.kumar.ug23@nsut.ac.in)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-4C1D95?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/rajvardhankumar)
[![GitHub](https://img.shields.io/badge/GitHub-312E81?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rajvardhan-git-sys)

</div>

<div align="center">

*"Systems don't fail gracefully by accident — they fail gracefully because someone designed them to."*

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=20,11,6&height=120&section=footer" width="100%"/>

</div>
