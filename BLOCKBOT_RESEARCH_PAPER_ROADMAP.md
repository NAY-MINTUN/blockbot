# BlockBot Research Paper Roadmap

> **Recommended direction:** a mixed-method pilot usability and feasibility study of BlockBot for novice robotic-arm programming.
>
> **Primary academic domain:** Computing Education Research.
>
> **Secondary domains:** Human–Computer Interaction, Educational Technology, and Educational Robotics.
>
> **Important:** Do not recruit participants, record people, or collect study data until a teacher/supervisor has confirmed the institution’s ethics requirements. If participants are minors, parental/guardian consent and the minor’s assent are normally required.

---

## 1. Direct answer: can BlockBot become a research paper?

Yes. BlockBot can support a legitimate research paper, but the paper needs a research question, a systematic method, evidence, analysis, limitations, and a contribution to existing knowledge. The software alone is a project artifact; describing how it was built is a project report. It becomes research when the artifact is used to investigate a clearly defined question.

The most defensible claim is not that BlockBot invents a new type of robot. Blockly, WebSockets, ESP32 boards, PWM controllers, and hobby servos already exist. The potential contribution is the way these elements are integrated for novice programming and the evidence collected about whether the resulting interface is usable and educationally meaningful.

The best achievable paper is:

> **Design and Pilot Usability Evaluation of BlockBot: A Block-Based Interface for Novice Robotic-Arm Programming**

This paper would ask whether programming beginners can use BlockBot to create and execute increasingly complex arm-motion programs, what difficulties they experience, and how they perceive the system’s usability.

This is a realistic paper for a school project because:

- the functional prototype already exists;
- it can be evaluated without developing a new control algorithm;
- objective task data and qualitative feedback can be collected in short sessions;
- the study can be presented as a pilot, avoiding unsupported claims of universal learning effectiveness; and
- the outcome naturally fits a poster, student conference, work-in-progress paper, or short research paper.

---

## 2. The distinction between exposure, publication, and peer review

These terms are not equivalent. Confirm which one the committee accepts.

| Activity | Publicly visible? | Reviewed? | Usually considered a publication? | Strength as external exposure |
|---|---:|---:|---:|---|
| Public project webpage or repository | Yes | No | Usually no | Low to moderate |
| Public demo video | Yes | No | No | Low to moderate |
| School/external exhibition demonstration | Yes | Sometimes | Usually no | Moderate |
| Poster at an external student symposium | Yes | Often screened | Sometimes appears in abstracts/proceedings | Moderate to strong |
| Zenodo technical report/preprint with DOI | Yes | No peer review | Public research output, but not peer-reviewed | Moderate |
| Workshop or work-in-progress paper | Yes | Usually reviewed | Often yes, depending on proceedings | Strong |
| Conference full paper | Yes | Peer-reviewed | Yes | Strong |
| Journal article | Yes | Peer-reviewed | Yes | Strongest, but slowest and most demanding |

Publishing a PDF in a repository can make it public and citable, but it must not be described as “peer-reviewed” unless independent scholarly peer review actually happened. Zenodo automatically registers a DOI for published records, but Zenodo is a repository rather than a journal. Its documentation explains that records can contain publications, datasets, software, posters, and presentations and receive persistent identifiers: [Zenodo records and DOIs](https://help.zenodo.org/docs/deposit/about-records/).

### Question to ask the committee verbatim

> “Does the external-exposure requirement accept a publicly available technical report or preprint with a DOI, or must the paper be accepted by a peer-reviewed conference or journal before my final defense?”

Get the answer in writing if possible. Submission, acceptance, presentation, publication, and public deposit are five different milestones.

---

## 3. Recommended academic domain

### 3.1 Primary domain: Computing Education Research

BlockBot is fundamentally about helping novices express algorithms and programming structures through blocks. Appropriate topics include:

- introductory programming;
- block-based programming;
- computational thinking;
- programming misconceptions;
- debugging behavior;
- physical computing; and
- transition from visual instructions to physical action.

The ACM International Computing Education Research community explicitly includes pedagogical environments, attitudes and measurement, psychology of programming, and work-in-progress contributions. Its research guidance also emphasizes transparent participant descriptions and ethical treatment: [ACM ICER research guidance](https://icer2024.acm.org/track/icer-2024-papers).

### 3.2 Secondary domain: Human–Computer Interaction

If the main outcomes are task completion, time, errors, assistance, perceived usability, and user feedback, the paper is also an HCI usability study. Relevant HCI ideas are:

- learnability;
- effectiveness;
- efficiency;
- error prevention;
- system feedback;
- mental workload;
- accessibility; and
- user confidence.

### 3.3 Application domain: Educational Robotics

The physical robotic arm gives the programming activity a visible, tangible output. Educational-robotics literature often considers sequencing, looping, debugging, problem solving, and computational thinking. A recent review also cautions that uncontrolled single-group studies cannot establish causal learning effects, which supports describing this project as a pilot rather than claiming that BlockBot improves learning: [educational robotics review and risk-of-bias discussion](https://link.springer.com/article/10.1007/s44436-026-00039-1).

### 3.4 Supporting domain: Educational Technology

BlockBot is a technology-rich learning environment. This domain is appropriate if the paper focuses on classroom integration, instructional design, teacher observations, or student engagement. The International Journal of STEM Education, for example, explicitly covers technology-rich learning environments and innovative STEM pedagogy, but it expects systematic, empirically grounded work and should be considered a high-bar future venue rather than the easiest first publication: [journal scope](https://link.springer.com/article/10.1186/2196-7822-1-1).

### 3.5 Why IoT should not be the primary domain

BlockBot contains IoT-like elements—a Wi-Fi-connected embedded device, local WebSocket communication, and a browser controller—but it does not currently contain cloud device management, secure provisioning, telemetry storage, fleet management, or a novel IoT protocol. Calling it an IoT prototype is reasonable. Claiming a major IoT research contribution is not yet supported.

### 3.6 Why control engineering should not be the primary domain

The project uses linear angle-to-PWM mapping and fixed safety limits. It has no feedback sensor, trajectory controller, inverse kinematics, motion planning, or new control algorithm. A robotics-control paper would require significant additional hardware, mathematics, experiments, and comparison with existing control methods.

### Recommended keywords

Use five to seven of these, depending on the venue:

- block-based programming;
- educational robotics;
- computing education;
- computational thinking;
- visual programming;
- robotic arm;
- usability evaluation;
- physical computing;
- novice programmers; and
- human–robot interaction.

---

## 4. Paper types BlockBot could support

### Option A — Design and usability pilot: recommended

**Question:** Can novice users successfully create robotic-arm programs with BlockBot, and what usability barriers do they encounter?

**Evidence required:** supervised task sessions, completion results, timing, errors, assistance, a validated usability questionnaire, and short interviews.

**Difficulty:** moderate.

**Best output:** student conference paper, poster, short paper, demo paper, or work-in-progress track.

**Why it fits:** It evaluates the existing project directly and does not require a second interface or a long teaching intervention.

### Option B — Comparative interface experiment

**Question:** How does BlockBot’s visual interface compare with a text-based or manual command interface for novice robotic-arm programming?

**Evidence required:** two equivalent interfaces, equivalent task sets, counterbalanced condition order, enough participants for paired analysis, and controlled instruction.

**Difficulty:** high.

**Strength:** stronger evidence because there is a comparator.

**Main risk:** a poorly designed text interface creates an unfair comparison. The study would measure differences between two particular implementations, not prove that all block programming is better than all text programming.

### Option C — Learning-effectiveness study

**Question:** Does using BlockBot improve students’ understanding of sequencing, loops, and debugging?

**Evidence required:** a defined lesson, validated or carefully developed pre/post assessment, an appropriate comparison group if causal claims are intended, delayed retention testing if possible, and a larger sample.

**Difficulty:** high to very high.

**Main risk:** a one-session pre/post increase can result from repeated testing, instructor help, novelty, or test alignment. It does not by itself prove educational effectiveness.

### Option D — Technical architecture and performance paper

**Question:** What latency, reliability, validation behavior, and hardware timing does the local browser-to-ESP32 architecture achieve?

**Evidence required:** instrumented software acknowledgments, physical motion-onset measurements, repeated network trials, disconnection tests, PWM measurements, and reproducible test conditions.

**Difficulty:** moderate if suitable instruments are available.

**Best use:** fallback when human-participant approval is not possible.

**Weakness:** the architecture uses established technologies, so the paper needs careful experimental characterization or an educational-design contribution to avoid being only a build report.

### Option E — Safety and validation evaluation

**Question:** How effectively does layered backend and firmware validation prevent unsafe prototype commands?

**Evidence required:** a threat/failure model, malformed-command test matrix, boundary tests, direct-to-device tests, disconnect behavior, and documented physical-safety limitations.

**Difficulty:** moderate.

**Main risk:** software limits are not a certified safety system. The title and claims must make the prototype scope unmistakable.

### Option F — Accessibility study

**Question:** What barriers do users with particular accessibility needs encounter in BlockBot’s visual programming interface?

**Evidence required:** accessibility expertise, representative participants or expert evaluation, an accessible study procedure, and likely frontend changes.

**Difficulty:** high and ethically sensitive.

**Potential:** meaningful, because block interfaces are not automatically accessible. Google’s Blockly work specifically identifies keyboard, screen-reader, low-vision, motor, and multimodal access as active design areas: [Blockly accessibility overview](https://developers.google.com/blockly/accessibility).

### Option G — Design case study or experience report

**Question:** What design decisions and engineering lessons arise when building a low-cost block-programmed arm for a school context?

**Evidence required:** design rationale, iteration history, observed failures, test evidence, and lessons that generalize beyond this single project.

**Difficulty:** low to moderate.

**Strength:** feasible with limited participant access.

**Weakness:** many journals will not treat a descriptive artifact report as original empirical research. It fits posters, demos, practitioner venues, or student journals better.

### Option H — Systematic literature review

**Question:** What methods and outcomes have been used to evaluate block-based educational robotics for novice programmers?

**Evidence required:** a registered protocol, multiple scholarly databases, reproducible search strings, duplicate screening, quality appraisal, and structured synthesis.

**Difficulty:** deceptively high.

**Recommendation:** Do not select this merely because it avoids participants. A credible systematic review requires much more than summarizing papers found through Google.

### Decision matrix

| Paper type | Uses current prototype | Human approval | Extra development | Evidence strength | School-project feasibility |
|---|---:|---:|---:|---:|---:|
| Usability pilot | Yes | Yes | Small instrumentation | Moderate | **Highest** |
| Interface comparison | Partly | Yes | Significant | Strong | Medium |
| Learning effectiveness | Yes | Yes | Curriculum + assessment | Potentially strong | Low to medium |
| Technical performance | Yes | No humans | Instrumentation | Moderate | High |
| Safety/validation | Yes | No humans | Test harness | Moderate | High |
| Accessibility | Yes | Usually | Significant | Potentially strong | Low |
| Design case study | Yes | Possibly no | Minimal | Low to moderate | High |
| Systematic review | Not required | No | Major literature work | Depends on rigor | Medium |

---

## 5. The exact recommended study

### 5.1 Proposed title

**Design and Pilot Usability Evaluation of BlockBot: A Block-Based Interface for Novice Robotic-Arm Programming**

Alternative titles:

1. **BlockBot: Exploring the Usability of Block-Based Robotic-Arm Programming for Novices**
2. **From Visual Blocks to Physical Motion: A Mixed-Method Evaluation of BlockBot**
3. **Evaluating a Browser-Based Visual Programming Interface for a Low-Cost Robotic Arm**
4. **BlockBot as a Physical-Computing Learning Tool: Design and Preliminary User Evaluation**
5. **A Local Web Architecture for Beginner-Oriented Block Programming of a Four-Servo Robotic Arm**

Use “pilot,” “preliminary,” or “exploratory” when the sample is small. Those words accurately limit the claim.

### 5.2 Aim

To evaluate whether programming novices can use BlockBot to construct and execute basic robotic-arm programs and to identify usability strengths, errors, and improvement opportunities.

### 5.3 Research questions

**RQ1 — Task effectiveness:** To what extent can novice users complete predefined robotic-arm programming tasks with BlockBot?

**RQ2 — Efficiency and assistance:** How much time, assistance, and how many observable errors are associated with each task?

**RQ3 — Perceived usability:** How do participants rate the overall usability of BlockBot after completing the tasks?

**RQ4 — User experience:** What interface features do participants identify as helpful, confusing, or missing?

These are descriptive and exploratory questions. They do not claim that BlockBot causes learning or is better than another system.

### 5.4 Optional hypotheses

The recommended pilot does not require null-hypothesis significance tests. If the institution insists on hypotheses, use pre-specified feasibility statements rather than invented superiority claims. Example:

- H1: Most participants will independently complete the basic single-movement task.
- H2: Participants will be able to complete a sequence involving movement and waiting after a short standardized introduction.

The words “most,” “independently,” “complete,” “basic,” and “short” must be numerically or operationally defined before data collection. Do not choose thresholds after seeing results.

### 5.5 Contribution statement

A defensible contribution statement is:

> This work contributes (1) the design and implementation of a browser-based block language connected to a physical four-servo robotic arm, (2) a documented local architecture with layered command validation, and (3) pilot evidence about novice task performance and usability barriers that can guide future educational-robotics interfaces.

Do not use “first,” “unique,” “revolutionary,” or “proves” unless a comprehensive literature search and evidence genuinely justify the term.

---

## 6. Study design

### 6.1 Overall design

Use a **single-session, one-group, mixed-method usability study**:

- **quantitative:** task success, completion time, error count, help level, and usability questionnaire;
- **qualitative:** observation notes and a short post-session interview; and
- **technical:** connection failures and command errors recorded by the system or researcher.

This design evaluates feasibility and usability. It cannot establish long-term learning or causal superiority.

### 6.2 Participants

Recommended target population:

- people with little or no prior robotics programming experience;
- able to understand the study language;
- familiar with basic computer or tablet interaction; and
- preferably 18 or older for the simplest consent process.

Record relevant background without collecting unnecessary identity data:

- age range rather than exact birth date;
- education level;
- prior text-programming experience;
- prior block-programming experience;
- prior robotics experience;
- frequency of computer use; and
- optional self-rated confidence with programming.

### 6.3 Sample size

There is no universally correct sample size. It depends on the primary outcome and intended claim.

| Goal | Practical range | What may be claimed |
|---|---:|---|
| Find major qualitative interface problems | About 5–8 representative users | Problems observed in this usability round; not population percentages. |
| Exploratory mixed-method pilot | About 15–25 users | Preliminary task/usability patterns with uncertainty and limited generalizability. |
| More stable quantitative usability estimates | Often 30–40+ | More useful confidence intervals, depending on variability and design. |
| Comparative experiment | Determine by an a priori power/precision analysis | A difference between the tested conditions, if design assumptions are met. |

Usability guidance distinguishes small qualitative studies from quantitative studies that seek population estimates; small samples should not be used for confident percentages or broad generalization: [qualitative versus quantitative sample reasoning](https://www.nngroup.com/articles/5-test-users-qual-quant/). For a school pilot, 15–25 adult novices can be a practical target, but this is not an automatic guarantee of publication. If recruitment is smaller, present the work as qualitative formative evaluation or a case series rather than pretending the statistics are precise.

The final sample target must be selected with the supervisor before data collection. Record expected exclusions and whether replacement participants will be recruited.

### 6.4 Recruitment

Use a neutral invitation that states:

- the purpose in plain language;
- approximate duration;
- that participation is voluntary;
- that declining has no effect on grades, employment, or relationships;
- whether compensation exists;
- what data are collected;
- whether photos/video are optional; and
- contact details for questions.

Avoid recruiting people over whom the researcher has authority. If classmates are recruited, make clear that teachers will not see individual responses and participation will not affect assessment.

### 6.5 Inclusion and exclusion rules

Define these before recruitment.

Example inclusion rules:

- within the approved age range;
- provides valid informed consent;
- fits the stated novice profile; and
- can use the interface with available accommodations.

Example exclusion rules:

- helped design or extensively test BlockBot;
- has already practiced the exact study tasks;
- does not provide consent; or
- a technical failure makes the full session impossible.

Do not quietly remove participants because their results are unfavorable. Report every exclusion and its pre-defined reason.

---

## 7. Ethics and participant protection

### 7.1 Approval comes before data

Ask the supervisor or school research office:

1. Is formal ethics or institutional review required?
2. Who is the responsible adult investigator if the student researcher is a minor?
3. Can classmates be recruited?
4. Are minors allowed, and what parent/guardian documents are required?
5. Can sessions be photographed, audio-recorded, or screen-recorded?
6. Where may anonymized data be stored?
7. How long must data be retained and when must it be destroyed?
8. Can anonymized data be publicly shared?

ACM publication policy requires research involving people to follow applicable ethical/legal standards, minimize harm, protect privacy and self-determination, and use informed consent. Publications may ask for participant selection, consent, treatment, and data-sharing details. Research involving children commonly also requires guardian consent and the child’s assent: [example ACM human-participant requirements](https://chiplay.acm.org/2026/full-papers/).

### 7.2 Consent versus assent

- **Consent:** legally valid agreement by an adult participant or a minor’s parent/guardian.
- **Assent:** the minor participant’s own understandable and voluntary agreement.

A parent’s consent does not justify forcing an unwilling child to participate.

### 7.3 Minimal-risk procedure

- Keep participants outside the arm’s movement envelope.
- The researcher controls electrical power.
- Use conservative tested movements without a payload.
- Stop immediately if hardware behaves unexpectedly.
- Do not collect sensitive personal information.
- Permit withdrawal without penalty.
- Make photographs, audio, and video separate optional choices.
- Do not show identifiable faces in publications without explicit permission.

### 7.4 Data protection

Assign IDs such as `P01`, `P02`, and `P03`. Keep any consent forms separately from response data. The analysis file should not contain names, emails, student numbers, or exact birth dates.

Recommended separation:

```text
consent/              restricted; real names; never public
raw-private/          restricted observations or recordings
analysis-anonymized/  participant IDs only
public-data/          only after disclosure review and approval
```

Do not promise anonymous data if the session is video-recorded or the researcher knows the participant. “Confidential and de-identified during analysis” is usually more accurate.

### 7.5 AI-use disclosure

Every target venue has its own rules. AI systems cannot take responsibility for the work and should not be listed as authors. Record how AI was used, verify every statement and citation, and disclose its use if the venue requires it. Never submit invented citations, invented participant data, or AI-generated quotations as real evidence.

---

## 8. Apparatus and controlled setup

Document the exact setup so another researcher could understand or reproduce it:

- computer model and operating system;
- browser and exact version;
- screen size and resolution;
- input method: mouse, trackpad, or touchscreen;
- network: router/hotspot model if relevant;
- approximate distance from access point;
- ESP32 board model and MicroPython version;
- PCA9685 board and I²C address;
- servo models and channel mapping;
- arm dimensions;
- servo-supply voltage/current rating;
- BlockBot commit identifier or release version;
- backend dependency versions;
- Blockly version;
- location, lighting, noise, and seating;
- whether the researcher stood nearby;
- whether participants saw physical motion directly; and
- safety arrangement and power-disconnect method.

Use the same setup for all participants unless the research question studies multiple devices. Record every deviation.

### Freeze a study version

Before the first participant:

1. fix known critical defects;
2. tag a release such as `study-v1.0`;
3. archive the version;
4. test all tasks;
5. do not change the interface mid-study; and
6. if a serious safety fix is required, document the version split and its effect.

Changing the UI after several participants creates different experimental conditions.

---

## 9. Study tasks

The tasks should measure realistic use without telling participants exactly which blocks to drag.

### Task 0 — orientation, not scored

The researcher provides the same short introduction to everyone:

- identify the toolbox and workspace;
- show how blocks connect and disconnect;
- explain the four joint names;
- explain that every program starts with `when run`;
- show New and Run; and
- state physical safety rules.

Do not demonstrate the exact solution to a scored task.

### Task 1 — single movement

**Instruction:** “Create and run a program that moves the base to 90 degrees.”

**Purpose:** tests discovery of the start block, movement block, dropdown, angle entry, block connection, and Run.

**Exact success:** a start-rooted program sends channel 0 at 90°, produces the expected visible movement, and is run without the researcher constructing it.

**Suggested maximum:** choose and preregister a limit such as 3 minutes.

### Task 2 — ordered sequence and waiting

**Instruction:** “Move the base to 70 degrees, wait one second, and then move the base to 110 degrees.”

**Purpose:** tests sequencing, wait placement, and understanding that connected order becomes execution order.

**Exact success:** the three commands are in the specified order and the visible pause occurs between the two movements.

**Suggested maximum:** choose and preregister a limit such as 5 minutes.

### Task 3 — repetition

**Instruction:** “Create a program that repeats this gripper action twice: move to 100 degrees, wait half a second, then move to 130 degrees and wait half a second.”

**Purpose:** tests discovery and nesting of the standard repeat block plus custom robot blocks.

**Exact success:** a repeat count of two encloses the requested ordered sequence and execution remains within the gripper’s 90°–150° limit.

**Suggested maximum:** choose and preregister a limit such as 7 minutes.

### Optional Task 4 — recovery/debugging

Give the participant a prebuilt workspace containing one deliberate mistake, such as a movement block not connected to `when run`, and ask them to make it work.

This tests debugging, but the mistake must be identical for every participant and the expected correction must be defined in advance.

### Avoid unsafe or unfair tasks

- Do not ask for an out-of-range movement just to “see what happens” on live mechanics.
- Do not change wording between participants.
- Do not give some participants extra hints unless the assistance level records it.
- Do not use a complex first task merely to create dramatic improvement later.
- Do not count a researcher-completed solution as independent participant success.

---

## 10. Operational definitions and observation sheet

### 10.1 Task outcome

Use separate fields rather than one vague successful/unsuccessful label:

- `completed_exactly`: yes/no;
- `within_time_limit`: yes/no;
- `program_ran`: yes/no;
- `physical_output_as_expected`: yes/no;
- `assistance_level`: 0–3;
- `completion_seconds`;
- `interface_errors`;
- `program_logic_errors`; and
- `technical_failures`.

### 10.2 Assistance scale

| Level | Definition |
|---:|---|
| 0 | No help after the task instruction. |
| 1 | General prompt without naming the solution, such as “Check where execution begins.” |
| 2 | Specific hint identifying the relevant block or area. |
| 3 | Researcher demonstrates or directly fixes part of the solution. |

State whether “independent completion” means level 0 only or allows level 1. Choose before collection.

### 10.3 Error taxonomy

| Error category | Example |
|---|---|
| Start/root error | Program blocks are not connected below `when run`. |
| Selection error | Wrong joint selected. |
| Parameter error | Wrong angle, wait time, or repeat count. |
| Sequence error | Correct blocks in the wrong order. |
| Nesting error | Repeat body is outside the loop. |
| Execution error | Participant does not press Run or presses New accidentally. |
| Interpretation error | Participant expects wait to move a joint or misunderstands a label. |
| Connection error | Blocks visually appear near each other but are not snapped together. |
| System error | Browser/backend/device disconnect unrelated to participant action. |
| Hardware error | Servo/power/mechanism fails despite correct software. |

Develop a one-page coding guide. If two observers code errors, train them on pilot sessions and report how disagreements were resolved.

### 10.4 Timing rules

- Start when the participant finishes reading the task and says they are ready.
- End when the required physical sequence finishes or the participant declares completion, depending on the preregistered definition.
- Pause timing only for researcher-confirmed technical failures.
- Record both raw duration and any paused duration.
- If think-aloud is used, acknowledge that speaking can affect completion time.

Retrospective questioning after each task is easier to interpret when time is an outcome.

---

## 11. Questionnaires and interview

### 11.1 Pre-study questionnaire

Keep it brief:

1. Participant ID assigned by researcher.
2. Age range.
3. Current education level.
4. Text-programming experience: none / introductory / intermediate / advanced.
5. Block-programming experience: none / once or twice / occasional / frequent.
6. Robotics experience: none / introductory / intermediate / advanced.
7. Primary input method normally used.
8. Optional self-rating: “How confident are you about creating a computer program?” on a defined five-point scale.

### 11.2 System Usability Scale

The System Usability Scale (SUS) is a ten-item global usability instrument introduced by John Brooke. Use the established wording and scoring from the original instrument rather than inventing a modified “SUS” while keeping the name: [Brooke’s SUS source](https://hci-studies.org/methods-and-measures/downloads/SUS_Brooke1996.pdf).

Scoring:

1. Responses use values 1–5.
2. For odd-numbered items, contribution = response − 1.
3. For even-numbered items, contribution = 5 − response.
4. Sum the ten contributions.
5. Multiply the sum by 2.5.

The result ranges from 0 to 100 but is not a percentage. Report the mean, standard deviation, confidence interval, median, and range as appropriate for the sample. Do not label a score “excellent” using an uncited graphic, and do not treat a convenient historical benchmark as a pass/fail law.

If the study is not in English, use a validated translation if available. Do not casually rewrite difficult terms, because changing item wording may change the instrument’s measurement properties.

### 11.3 Optional workload measure

NASA-TLX measures perceived workload across mental, physical, temporal, performance, effort, and frustration dimensions. The official package explains its dimensions and procedure: [NASA-TLX materials](https://humansystems.arc.nasa.gov/groups/tlx/downloads/TLX.pdf).

For the easiest study, use SUS plus task metrics and interviews. Add NASA-TLX only if workload is a research question; too many scales burden participants and encourage unfocused analysis.

### 11.4 Post-study interview questions

Ask the same core questions in the same order:

1. What was easiest about creating the programs?
2. What was most difficult or confusing?
3. Was any joint name, block label, icon, or message unclear?
4. How did seeing the physical arm move affect your understanding of the program?
5. What did you expect to happen when you pressed Run?
6. How did you decide where to place the wait block?
7. What would you change first?
8. Would you feel confident creating a new sequence without help? Why?
9. What feature did you expect but not find?
10. Is there anything else you want to say about the experience?

Avoid leading questions such as “Did the easy blocks help you learn better?”

---

## 12. Session protocol

### Proposed duration: approximately 30–40 minutes

| Stage | Approximate time | Procedure |
|---|---:|---|
| Welcome and safety | 2 min | Introduce researcher, voluntary participation, and arm safety. |
| Consent confirmation | 3 min | Answer questions and confirm recording choices. |
| Background survey | 3 min | Collect only approved demographic/experience fields. |
| Standard orientation | 5 min | Give identical interface introduction. |
| Task 1 | Up to set limit | Observe without unnecessary intervention. |
| Task 2 | Up to set limit | Record outcomes, time, errors, and help. |
| Task 3 | Up to set limit | Record outcomes, time, errors, and help. |
| SUS | 3 min | Participant answers privately. |
| Interview | 5–8 min | Ask standardized open questions and follow-ups. |
| Debrief | 2 min | Explain purpose, withdrawal/contact process, and next steps. |

### Researcher script principles

- Read scripted task wording.
- Remain neutral after success and failure.
- Use the defined assistance ladder.
- Never physically endanger the participant to preserve data.
- Record technical faults separately from user errors.
- Do not teach one participant more than another during scored tasks.
- Thank every participant without evaluating their ability.

### Pilot the protocol

Run one or two non-study pilot sessions before freezing the protocol. Pilot participants should not enter the final dataset unless the approved protocol explicitly permits it and no material changes were made. Use pilots to check:

- task clarity;
- realistic time limits;
- observation sheet usability;
- safe servo motion;
- questionnaire delivery;
- session duration; and
- data-export process.

---

## 13. Instrumentation required before the study

The current BlockBot application was designed as a prototype, not a research logger. Add a local, privacy-conscious event log before study sessions or use a precise observer sheet.

Recommended event fields:

```text
participant_id
session_id
study_version
task_id
event_timestamp_monotonic
event_type
channel
angle
wait_seconds
backend_reply_ok
error_category
connection_state
assistance_level
notes
```

Potential event types:

- `task_started`;
- `run_pressed`;
- `command_sent`;
- `backend_reply_received`;
- `command_rejected`;
- `socket_disconnected`;
- `socket_reconnected`;
- `task_completed`;
- `hint_given`; and
- `task_abandoned`.

### Important measurement limitation

BlockBot currently returns the browser’s successful reply after FastAPI validates and sends a command to the ESP32 connection. It does not prove that the ESP32 wrote the PCA9685 register or that a servo physically moved. Therefore:

- call it a **relay acknowledgment**, not a movement-completion acknowledgment;
- use direct observation or video timing for physical movement;
- or extend the firmware to send a device acknowledgment after its I²C write and relay that response back to the browser.

Even a device acknowledgment after I²C writing would not prove the servo reached the target. True completion evidence requires position feedback or an external measurement method.

### Timing correctly

Use a monotonic clock for durations. Wall-clock timestamps can jump if system time changes. If browser, backend, and ESP32 times are compared, synchronize them or measure round-trip timing from one clock.

### Privacy

Do not put participant names in application logs. Do not log Wi-Fi passwords, IP addresses unnecessarily, consent responses, or raw interview audio in the code repository.

---

## 14. Data structure

### Participant table

```csv
participant_id,age_band,education_level,text_experience,block_experience,robotics_experience
P01,18-20,secondary,none,introductory,none
```

The example is a schema illustration, not real data.

### Task table

```csv
participant_id,task_id,completed_exactly,within_limit,time_seconds,assistance_level,interface_errors,logic_errors,technical_failures
P01,T1,true,true,85,0,0,0,0
```

Never leave fabricated example rows in the analysis dataset. Clearly label templates.

### SUS table

Store item responses and the calculated total:

```text
participant_id, sus_1 ... sus_10, sus_total
```

Retaining item values enables scoring verification. Reverse-score only during analysis and test the scoring code with known examples.

### Qualitative table

```text
participant_id | question_id | deidentified_response | initial_code | theme | analyst_note
```

Remove personal names, school identifiers, and third-party information from quotations.

---

## 15. Analysis plan

Write and approve this plan before viewing final outcomes.

### 15.1 Descriptive participant analysis

Report:

- number recruited;
- number consented;
- number who completed;
- exclusions with reasons;
- age bands;
- education level; and
- previous programming/robotics experience.

Do not imply that convenience-sampled classmates represent all students.

### 15.2 Task effectiveness

For each task, report:

- independent exact completion count and proportion;
- completion with any assistance;
- timeout or abandonment count;
- physical-output success;
- technical-failure count; and
- a confidence interval for a proportion when the sample supports it.

Wilson confidence intervals are generally more suitable than the simple normal approximation for small binomial samples. State the method and confidence level.

### 15.3 Efficiency

Task-time data are often skewed. Report:

- median;
- interquartile range;
- minimum and maximum; and
- mean and standard deviation only as supplementary descriptions when useful.

Define how timeouts are represented. Do not replace them silently with the maximum time and then analyze the values as ordinary completions without explanation.

### 15.4 Error and assistance analysis

Report errors by task and category. A useful table is:

| Error type | T1 count | T2 count | T3 count | Participants affected |
|---|---:|---:|---:|---:|

Report assistance-level distributions separately. A participant completing after a direct demonstration is not equivalent to an independent completion.

### 15.5 SUS analysis

- Verify each row has all ten allowed responses.
- Calculate totals with a tested formula.
- Report mean, standard deviation, median, range, and a confidence interval.
- Show individual scores in a de-identified dot plot if the sample is small.
- Do not report excessive decimal places.
- Do not claim the score proves educational effectiveness; SUS measures perceived usability.

### 15.6 Qualitative analysis

For a manageable school study:

1. transcribe or summarize responses consistently;
2. read all responses before finalizing codes;
3. assign short codes to meaningful statements;
4. group related codes into themes;
5. search for statements that contradict the emerging interpretation;
6. select brief de-identified quotations;
7. explain who coded the data; and
8. preserve an audit trail of codebook revisions.

Possible themes must emerge from data. Do not decide in advance that participants found BlockBot “easy and engaging.” Examples such as label clarity, physical feedback, block connection difficulty, or desire for a stop button can be provisional sensitizing concepts, not predetermined findings.

### 15.7 Mixed-method integration

Connect the quantitative and qualitative evidence:

- If task completion is high but interviews report uncertainty, discuss the difference.
- If the loop task takes longer, use observations to identify whether nesting or terminology contributed.
- If SUS is favorable but users request a Stop button, distinguish overall usability from a critical missing control.
- If a technical disconnect causes failure, do not code it as participant inability.

### 15.8 Statistical restraint

For a one-group pilot:

- prioritize estimates, plots, and confidence intervals;
- do not test every variable against every demographic;
- do not treat p > .05 as proof of no difference;
- do not interpret task-to-task time differences as learning because task difficulty changes; and
- do not make population-wide claims from a convenience sample.

### 15.9 If a future comparison is performed

For BlockBot versus text control:

- use a within-participant design if appropriate to reduce between-person variation;
- create equivalent A/B task sets;
- counterbalance interface order;
- standardize training;
- test for carryover/learning effects;
- select paired analysis based on distribution and measurement assumptions;
- report effect size and confidence interval, not p-value alone; and
- conduct an a priori power or precision calculation.

---

## 16. Validity threats

### Internal validity

- Participants improve simply through task order.
- Researcher hints vary by participant.
- Hardware or network faults look like usability problems.
- Participants behave differently because they are observed.
- The researcher who built the system unconsciously guides users.

Mitigation: fixed scripts, assistance coding, piloting, frozen software, technical-failure fields, and preferably an observer who did not build the interface.

### Construct validity

- Task success does not equal programming knowledge.
- SUS does not measure learning.
- A fixed wait does not measure motor completion.
- Relay acknowledgment does not prove physical action.
- “Engagement” cannot be established from one casual question.

Mitigation: align every claim with a measurement that actually represents it.

### External validity

- One school, one language, and convenience sampling limit generalization.
- Adult peers may not represent younger target learners.
- One arm and network setup may not represent other hardware.
- A short laboratory task may not represent classroom use.

Mitigation: describe context precisely and call the findings preliminary.

### Reliability

- Observers may classify errors differently.
- Timing may start or stop inconsistently.
- Servo behavior can vary with power and load.

Mitigation: operational definitions, observer training, standard setup, calibrated timing, and duplicate coding where feasible.

### Researcher bias

The developer wants the system to succeed. This can influence hints, notes, interview prompts, or interpretation.

Mitigation: preregistration, neutral scripts, raw result preservation, negative-case analysis, supervisor review, and transparent reporting of the researcher’s dual role.

---

## 17. Literature review plan

### 17.1 Concepts to review

1. block-based visual programming;
2. novice programming and syntax barriers;
3. computational thinking;
4. constructionism and learning through artifacts;
5. educational robotics and physical computing;
6. usability and learnability;
7. Blockly language design;
8. browser-to-embedded-device architectures; and
9. limitations of short educational interventions.

### 17.2 Databases

Use multiple scholarly sources if available:

- ACM Digital Library;
- IEEE Xplore;
- ERIC;
- Scopus or Web of Science through the institution;
- SpringerLink;
- ScienceDirect;
- Google Scholar for discovery and citation chaining; and
- the school library catalogue.

### 17.3 Search strings

Adapt syntax per database:

```text
("block-based programming" OR Blockly OR "visual programming")
AND (robot* OR "robotic arm" OR "physical computing")
AND (education OR novice OR student)
```

```text
("educational robotics" AND "computational thinking")
AND (usability OR evaluation OR learning)
```

```text
(Blockly AND robot* AND interface)
```

```text
("block programming" AND "text programming")
AND (novice OR beginner)
```

```text
("robot programming" AND usability AND student)
```

### 17.4 Screening criteria

Possible inclusion criteria:

- peer-reviewed articles or respected proceedings;
- directly concerns block programming, educational robotics, or novice physical computing;
- reports design guidance or empirical evaluation;
- language the research team can analyze accurately; and
- full text is available.

Possible exclusion criteria:

- robot use without programming activity;
- purely industrial manipulator control with no educational/HCI relevance;
- promotional product material presented as evidence;
- duplicate versions of the same study; and
- papers whose methods or results cannot support the claim for which they are cited.

### 17.5 Literature matrix

Create a spreadsheet with:

```text
citation | year | country/context | participants | age | system | design |
research_question | measures | main_findings | limitations | relevance_to_BlockBot
```

### 17.6 Establishing a gap

Do not decide the gap first and search only for support. After the literature matrix, ask:

- Which age groups have been studied?
- Which robotic platforms dominate?
- Are physical arms less studied than mobile robots?
- Are studies measuring usability, learning, or engagement?
- Do they report technical architecture and validation?
- Do they study local low-cost systems in settings similar to yours?
- Which limitations repeat across studies?

A safe gap statement might be:

> “Although block-based educational robotics has been widely explored, the usability of this particular browser-to-physical-arm design and the barriers novices encounter in creating joint-motion sequences have not yet been evaluated.”

That statement concerns BlockBot itself. A broader “no one has studied this” claim requires much stronger evidence.

### 17.7 Starting sources

- Google’s Blockly paper explains that Blockly supplies a visual grammar and code-generation framework, while application developers must design the vocabulary and runtime for their audience: [Tips for Creating a Block Language with Blockly](https://developers.google.com/static/blockly/publications/papers/TipsForCreatingABlockLanguage.pdf).
- A Blockly UX paper discusses lessons about block discoverability, instruction design, and progression toward text programming: [Ten Things We’ve Learned from Blockly](https://developers.google.com/static/blockly/publications/papers/TenThingsWeveLearnedFromBlockly.pdf).
- A global review discusses programming and computational-thinking education: [Frontiers in Computer Science review](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2022.997222/full).
- Research on student–robot interaction emphasizes examining what learners actually do when a robot behaves unexpectedly and how they debug: [student–robot interaction in robotics education](https://link.springer.com/article/10.1007/s10798-021-09677-3).
- A recent educational-robotics review gives a useful warning about causal claims from uncontrolled designs: [review of educational robotics outcomes](https://link.springer.com/article/10.1007/s44436-026-00039-1).

Read and cite the actual papers, not only search snippets. Verify bibliographic metadata with the publisher or DOI.

---

## 18. Paper structure

For a short 4,000–6,000-word paper, adjust to the target venue’s template.

### Title

State the artifact, population/context, and study type. Avoid promotional language.

### Abstract: approximately 150–250 words

Use five moves:

1. context/problem;
2. gap;
3. system and method;
4. actual results; and
5. contribution/limitation.

Do not write final numerical results before data collection.

Abstract template:

> Block-based programming can reduce syntax barriers in introductory computing, while educational robots provide visible physical feedback. However, the usability barriers novices encounter when programming a multi-joint arm through a browser require empirical examination. We present BlockBot, a prototype that combines a Blockly interface, a local FastAPI relay, and ESP32/PCA9685 servo control. We conducted a mixed-method pilot study with [N] novice participants who completed [number] programming tasks of increasing complexity. We measured task completion, time, errors, assistance, and perceived usability and analyzed post-session responses. [Insert factual results with uncertainty.] Findings indicate [bounded interpretation], while [main limitation or usability issue] requires further development. The work contributes an evaluated educational-robotics interface and design implications for novice block-based control of physical devices.

### 1. Introduction: approximately 600–800 words

- Explain the novice-programming problem.
- Explain why physical robotics may be useful.
- Identify what prior work covers.
- State the narrow gap.
- Introduce BlockBot in one paragraph.
- State RQs.
- List contributions.

### 2. Related work: approximately 700–1,000 words

Organize by ideas rather than one paragraph per paper:

1. block-based programming for novices;
2. educational robotics and computational thinking;
3. visual language/usability design; and
4. gap and positioning of BlockBot.

Compare studies’ participants, methods, and outcomes. Do not merely state that each author “found positive results.”

### 3. System design: approximately 700–900 words

- design goals;
- target user;
- custom blocks;
- execution model;
- browser/backend/ESP32 architecture;
- JSON protocol;
- hardware;
- safety limits;
- local prototype scope; and
- important limitations.

Include one architecture figure and one interface figure. Do not fill the paper with code screenshots.

### 4. Method: approximately 900–1,200 words

- study design;
- ethical approval/consent statement;
- participants and recruitment;
- apparatus;
- task design;
- measures;
- procedure;
- analysis plan; and
- data exclusions.

The method should make replication possible.

### 5. Results: approximately 700–1,000 words

Present evidence without explaining it away:

- participant flow/background;
- completion outcomes;
- times;
- errors/assistance;
- SUS;
- themes and quotations; and
- technical failures.

Results should not introduce methods that were never described.

### 6. Discussion: approximately 800–1,000 words

- answer each RQ;
- connect results to previous literature;
- explain design implications;
- discuss surprising or contradictory findings;
- distinguish observation from interpretation;
- identify validity threats; and
- state what cannot be concluded.

### 7. Limitations: approximately 250–400 words

Include convenience sample, short exposure, single site, developer-researcher role, prototype hardware, open-loop movement, and lack of comparison group.

### 8. Conclusion: approximately 150–250 words

Restate the contribution and bounded finding. Do not introduce new results or turn a pilot into proof of effectiveness.

### Other required sections

Depending on venue:

- ethics statement;
- informed consent;
- data availability;
- software availability;
- author contributions;
- conflicts of interest;
- funding;
- acknowledgments;
- AI-tool disclosure; and
- references.

---

## 19. Figures and tables

### Recommended figures

1. **System architecture:** browser → FastAPI → ESP32 → PCA9685 → servo.
2. **BlockBot interface:** a clean screenshot with numbered callouts.
3. **Study flow:** recruitment → orientation → tasks → SUS → interview.
4. **Task results:** participant-level completion/assistance plot.
5. **Task time distribution:** dot/box plot rather than only bars.

### Recommended tables

1. Hardware/software configuration.
2. Safe joint ranges and channel mapping.
3. Participant background.
4. Task definitions and success criteria.
5. Completion, time, errors, and help by task.
6. Qualitative themes with de-identified examples.
7. Limitations and planned mitigations.

### Figure integrity

- Use readable labels at final paper size.
- Do not use color as the only distinction.
- Add descriptive captions.
- Do not manipulate photographs in a way that changes evidence.
- Blur/remove personal information.
- Obtain permission for identifiable people and third-party assets.

---

## 20. Expected claim boundaries

### Claims the pilot may support

- Participants in this sample completed specified tasks at reported rates.
- Certain error categories occurred under the study conditions.
- Participants reported a particular SUS distribution.
- Interviews identified specific perceived strengths and barriers.
- The local architecture successfully supported the reported sessions, subject to documented faults.

### Claims it cannot support by itself

- BlockBot improves computational thinking.
- BlockBot is better than text programming.
- BlockBot works for all students.
- BlockBot is production-ready.
- BlockBot is safe for unsupervised use.
- Participants learned long-term robotics skills.
- High satisfaction caused better learning.
- A relayed command means a servo reached its angle.

Use phrases such as “in this pilot,” “among the participants studied,” “suggests,” “was associated with,” and “warrants further evaluation.”

---

## 21. Publication strategy

### Route 1 — fastest credible external exposure

1. Complete supervisor and ethics review.
2. Run a small but rigorous pilot.
3. Write a technical report or short paper.
4. Present a poster/demo at an external school, university, maker, STEM, or student-research event.
5. If the committee accepts it, archive the final public report, poster, software release, and anonymized materials on Zenodo.

Zenodo’s deposit workflow supports publications, datasets, software, posters, and presentations and can reserve or issue a DOI: [official upload instructions](https://help.zenodo.org/docs/deposit/create-new-upload/).

### Route 2 — peer-reviewed student/work-in-progress paper

Target, in this order:

1. an institutionally recognized student research conference;
2. a regional computing/STEM education conference;
3. a work-in-progress, poster, or demo track at an established computing-education/HCI venue; or
4. an educational-technology student journal with transparent review.

This route is the best balance of achievable scope and genuine scholarly review.

### Route 3 — full conference or journal paper

Pursue only if there is enough time, supervision, participant access, and methodological strength. Potential communities include computing education, engineering education, educational robotics, HCI, and STEM education. Examples to investigate—not promises of fit or acceptance—include ACM computing-education venues, IEEE education conferences, and established STEM/technology-education journals.

Calls, deadlines, page limits, fees, AI rules, preprint rules, and review tracks change. Verify every requirement on the official venue website immediately before preparing the submission.

### Recommended two-output plan

- **Output A:** externally presented poster or short paper for the school requirement.
- **Output B:** public archival package containing the report, poster, versioned software, protocol, and approved anonymized materials.

This gives both human-facing exposure and a permanent citable record. It still must not be called peer-reviewed unless Output A was peer-reviewed.

---

## 22. Selecting a legitimate venue

### Positive signs

- clear scope matching the paper;
- named editorial/program committee with verifiable affiliations;
- clear peer-review process;
- realistic review schedule;
- complete author instructions;
- transparent fees before submission;
- publication ethics, correction, and retraction policies;
- established publisher, society, university, or conference series;
- verifiable prior proceedings/articles; and
- DOI/ISSN and indexing claims that can be independently checked.

The Directory of Open Access Journals requires journals to state their peer-review process and normally use at least two independent reviewers, and it examines editorial boards, ethics, and journal operations: [DOAJ quality criteria](https://doaj.org/apply/guide/).

### Warning signs

- unsolicited flattering email promising acceptance;
- guaranteed publication;
- acceptance in a few days;
- scope covering almost every academic subject;
- hidden or changing fees;
- fake metrics;
- editors who cannot be verified;
- copied website content;
- no retraction or ethics policy;
- pressure to pay immediately; and
- a journal title designed to imitate a respected publication.

COPE identifies unclear fees, missing ethics policies, questionable editorial information, and implausible review practices as warning signs: [COPE guidance on deceptive publishing](https://publicationethics.org/files/cope_dd_a4_pred_publishing_nov19_screenaw.pdf).

### Before paying or submitting

Ask the supervisor or librarian to verify:

- the venue’s official domain;
- whether the school recognizes it;
- current indexing directly in the claimed database;
- all fees and waivers;
- copyright/license terms;
- whether a preprint is allowed;
- whether code/data links break anonymous review;
- average timeline without relying on promises; and
- whether the same manuscript can legally remain in a repository.

Do not submit the same manuscript to two peer-reviewed venues simultaneously.

---

## 23. Open research package

Only share files approved for release.

Suggested package:

```text
paper/
  blockbot-paper.pdf
  references.bib
poster/
  blockbot-poster.pdf
protocol/
  study-protocol.pdf
  task-script.pdf
  observation-sheet.pdf
  questionnaire-information.txt
analysis/
  README.md
  analysis-script.*
  anonymized-data.csv
software/
  source-release.zip
  VERSION.txt
LICENSES/
  software-license.txt
  document-license.txt
```

Before publishing source code:

- confirm `config.py` and Wi-Fi credentials are absent;
- remove IP addresses that should not be public;
- remove participant logs and recordings;
- verify rights to the logo and every third-party asset;
- preserve notices for vendored Microdot and Blockly dependencies;
- select an explicit software license with supervisor advice; and
- use a separate content/data license if appropriate.

Zenodo defaults to CC BY 4.0 for deposits but permits other licenses and mixed-license declarations, so choose deliberately rather than accepting a default without understanding it: [Zenodo license documentation](https://help.zenodo.org/docs/deposit/describe-records/licenses/).

### Preregistration

A preregistration records research questions, exclusions, outcomes, and analysis before results are known. It reduces the temptation to redefine the study after seeing data. If the institution supports OSF or another registry, preregister the approved protocol. Preregistration does not replace ethics approval.

---

## 24. Reproducibility checklist

Before submission, confirm that the paper states:

- exact BlockBot version/commit;
- all software dependency versions;
- hardware model and wiring;
- safe angle ranges;
- network configuration at an appropriate non-sensitive level;
- recruitment method;
- inclusion/exclusion rules;
- consent/ethics process;
- task wording;
- assistance policy;
- timing rules;
- outcome definitions;
- questionnaire/scoring source;
- missing-data handling;
- statistical methods;
- qualitative coding process;
- technical failures;
- deviations from protocol;
- data/code availability; and
- limitations.

Reproducibility means enough detail to understand and repeat the method; it does not justify publishing private participant data.

---

## 25. Eight-to-twelve-week working schedule

This is a planning example, not a promise of peer-review completion.

### Week 1 — confirm requirement and supervision

- Obtain the exact definition of external exposure.
- Identify teacher/supervisor and authorship roles.
- Choose the recommended usability pilot or technical fallback.
- Identify the institution’s ethics process.

### Week 2 — focused literature review

- Run documented searches.
- Build a literature matrix.
- Refine the gap, RQs, and contribution.
- Select validated measures.

### Week 3 — protocol and materials

- Draft consent/information materials.
- Define participants, tasks, outcomes, assistance, and analysis.
- Prepare observation sheets and interview questions.
- Submit for ethics/school approval.

### Week 4 — stabilize BlockBot

- Fix only study-critical issues.
- Add research logging if approved.
- Bundle Blockly locally if demonstration internet is uncertain.
- Freeze and tag the study version.
- Test power and mechanical safety.

### Week 5 — pilot

- Conduct one or two protocol pilots.
- Revise unclear instructions before formal collection.
- Freeze final materials.
- Update ethics documentation if required.

### Weeks 6–7 — collect data

- Follow the same procedure for every participant.
- Back up encrypted/restricted data.
- Keep a deviation and technical-failure log.
- Do not analyze selectively while deciding whom to recruit.

### Week 8 — clean and analyze

- De-identify data.
- Verify scoring.
- Create tables/plots.
- Code interviews.
- Integrate quantitative and qualitative results.

### Weeks 9–10 — write

- Method and results first.
- Then system design and related work.
- Write discussion and limitations.
- Write abstract last.

### Week 11 — internal review

- Supervisor checks claims, methods, citations, and ethics wording.
- Another reader checks whether the paper is understandable.
- Verify every reference and figure.

### Week 12 — external output

- Submit/present through the chosen legitimate route.
- Archive only what policies and consent permit.
- Record submission, acceptance, presentation, and publication evidence separately.

Peer review can take months and may require revision. If the defense deadline is close, do not assume that journal acceptance will happen in time.

---

## 26. Fallback paper without human participants

If approval or recruitment is impossible, use:

**Technical Evaluation of a Local Web-to-Embedded Architecture for Safe Prototype Control of a Four-Servo Robotic Arm**

### Research questions

- RQ1: Does backend validation correctly accept and reject all defined command classes and boundary values?
- RQ2: What browser-to-relay and relay-to-device timing is observed under controlled local-network conditions?
- RQ3: How reliably does the system recover from browser, backend, and device disconnections?
- RQ4: Do the PCA9685 outputs correspond to calculated pulse counts across representative angles?

### Required experiments

1. **Validation matrix:** every channel, boundary, just-inside, just-outside, wrong type, missing key, Boolean, malformed JSON, unknown command, and direct firmware input.
2. **PWM verification:** logic analyzer or oscilloscope readings at selected angles on every used channel.
3. **Timing:** many repeated trials, with warm-up policy, monotonic timestamps, network conditions, and distribution plots.
4. **Reliability:** controlled command batches with error counts; avoid claiming more cycles than actually run.
5. **Disconnect recovery:** browser loss, backend restart, ESP32 restart, access-point interruption, and changed device IP.
6. **Resource behavior:** ESP32 memory before/after server initialization if measured accurately.
7. **Safety analysis:** explicitly document that software limits are not industrial safety certification.

### Changes needed for sound measurement

- add a firmware acknowledgment after command parsing and I²C write;
- relay the device response rather than replying immediately after send;
- add command IDs;
- make firmware reject unknown channels and bad types;
- synchronize joystick and main limits;
- add test hooks or a simulated ESP32; and
- preserve raw logs and analysis scripts.

This route avoids participant ethics but still requires supervisor review, safe hardware procedures, and a genuine literature gap.

---

## 27. Questions the committee may ask about the research

**Why is this research and not only development?**  
The paper uses a defined protocol and measurements to answer questions about novice task performance and usability. The artifact is the instrument/context; the systematic evaluation provides the research evidence.

**What is the independent variable?**  
In the recommended one-group pilot there is no experimentally manipulated independent variable. Tasks provide structured contexts, and outcomes are descriptive. A later comparison would manipulate interface type.

**What are the dependent measures?**  
Exact task completion, time, errors, assistance, perceived usability, and qualitative feedback.

**Why not claim learning improvement?**  
The proposed study does not include a validated pre/post learning assessment, control condition, or retention test. Usability and task performance are not equivalent to learning.

**Why use mixed methods?**  
Counts and times show what happened; observations and interviews help explain why it happened. Their combination is more useful for improving an early prototype.

**Why are participants called novices?**  
Novice status is defined through stated eligibility and a background questionnaire, not assumed. The paper must report the actual experience distribution.

**How was sample size chosen?**  
It was selected before collection based on whether the goal was qualitative issue discovery, pilot estimation, or statistical comparison, and was limited transparently by recruitment feasibility.

**What is the primary outcome?**  
Choose one before collection. For this study, independent exact task completion across the predefined tasks is the clearest primary outcome.

**What is the major threat to validity?**  
The small convenience sample and developer-researcher role limit generalization and can introduce bias. Fixed scripts, preregistration, transparent assistance coding, and supervisor review reduce but do not eliminate that risk.

**What does the SUS measure?**  
It measures participants’ perceived overall usability. It does not directly measure learning, safety, or mechanical performance.

**Why is there no control group?**  
The first study is a feasibility/usability pilot intended to identify barriers and estimate performance, not prove superiority. Its results can justify and design a later controlled comparison.

**How do you know the servo moved correctly?**  
The current software acknowledgment does not establish physical position. The study uses direct observation for the expected action and clearly reports the lack of independent position sensing.

**Can results be generalized?**  
Only cautiously. They describe the sampled participants and test context. Broader claims require diverse sites, larger samples, and repeated classroom evaluation.

**What is novel?**  
Not the individual technologies. The contribution is the integrated novice-oriented design plus empirical evidence about its use and resulting design implications.

**Why publish a pilot?**  
Pilot work can expose methodological and interface problems, provide preliminary feasibility evidence, and establish a responsible basis for a larger study—as long as its claims remain limited.

**Was the work peer-reviewed?**  
Answer according to the actual route. A Zenodo DOI means public and citable, not peer-reviewed. A conference screening or poster acceptance should be described using the organizer’s exact review terminology.

**How did you prevent favorable-result bias?**  
Research questions, outcomes, exclusions, task wording, assistance rules, and analysis were fixed before collection; unfavorable cases and technical failures were retained and reported.

**Why this domain?**  
The research studies how novices program through a block interface, which is primarily computing education and HCI. The robot is the educational physical-computing context.

---

## 28. Immediate action checklist

Do these in order:

1. Ask the committee whether it requires public deposit, submission, acceptance, presentation, or peer-reviewed publication.
2. Ask a teacher or faculty member to supervise the research and ethics process.
3. Choose the usability pilot as the main design.
4. Restrict initial recruitment to consenting adults if that matches the research population and avoids an invalid mismatch with the intended users.
5. Complete the focused literature matrix before writing a novelty claim.
6. Finalize RQs, primary outcome, sample logic, tasks, assistance rules, and analysis.
7. Obtain required approval before recruitment or recording.
8. Freeze a safe study version of BlockBot.
9. Pilot the procedure with non-study volunteers.
10. Collect all cases consistently.
11. Analyze without changing definitions after seeing results.
12. Write bounded conclusions and full limitations.
13. Submit to a legitimate external poster/WIP/student venue.
14. Deposit an approved archival package only after checking venue and consent policies.
15. Keep documentary evidence of external exposure for the committee.

---

## 29. Final recommendation

Use BlockBot for a **pilot usability paper in Computing Education Research/HCI**, not a general IoT or robotics-control paper. Evaluate whether genuine novices can complete three defined programming tasks, record exact completion/time/error/assistance measures, administer SUS, conduct short interviews, and report the results as preliminary mixed-method evidence.

For the external-exposure requirement, aim first for a legitimate external student research poster, demo, or work-in-progress paper. If the committee accepts a public citable report, archive the approved paper and supporting materials on Zenodo for a DOI—but explicitly state that repository publication is not peer review. A later, stronger paper can compare BlockBot with a carefully designed text interface or evaluate learning through a controlled multi-session study.

This path is feasible, academically honest, and closely aligned with what the current prototype actually contributes.
