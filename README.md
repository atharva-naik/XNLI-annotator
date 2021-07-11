# XNLI-annotator
experimental annotation framework for phrase level annotation

Built using Flask, sqlite3, bootstrap and Javascript.

### Requirements:

python version >= 3.6 recommended <br>
This package requires flask

### Installation:

```git clone http://github.com/atharva-naik/XNLI-annotator```

### Instructions:
Please follow the steps below for annotation:

##### Register
Create a new user by clicking on the **Create** button on the **New User** tile, shown below, to keep track of your annotations. Immediately after creating your user you will be guided to the main annotation page.

<img src="https://github.com/atharva-naik/XNLI-annotator/blob/main/images/index.png" width="800"/>

<img src="https://github.com/atharva-naik/XNLI-annotator/blob/main/images/register.png" width="800"/>

##### Login Page
If you are already registered just click on the tile corresponding to your username and you will be guided to a login screen as shown below.

<img src="https://github.com/atharva-naik/XNLI-annotator/blob/main/images/login_page.png" width="800"/>

##### Main Annotation Page
How to use the main annotation page:

1. Phrase annotator: Just select a span of text and pick the label from ("Entail","Contradict","Neutral","Unaligned"). Clear P, Clear H can be used t o clear all marked phrases in the premise and hypothesis resepectively. Clear an be used to clear annotations form the selected span. Clear All clears all annotations. Press save to save the annotation.
2. Bookmarking: Save a particular annotation that you are doubtful about for later review. 
3. Navigate: Guides you to the navigation page.
3. Meaning: Select a word you, whose meaning you are unsure about. Click the button below, and the meaning will be shown in the "Meaning of selected word" area below.
4. Annotation sidebar: It shows the annotation that is currently saved on the server. It can be used to logout, open dashboard and view bookmarked annotations.
5. Instructions: Click on the ⓘ to view these instructions.

<img src="https://github.com/atharva-naik/XNLI-annotator/blob/main/images/annotation_page.png" width="800"/>

##### Navigation Pane
The navigation pane shows "Pending" or "Complete" beside each sentence-pair/sample. Use it to get a bird's eye view of your progress.

<img src="https://github.com/atharva-naik/XNLI-annotator/blob/main/images/navigation.png" width="800"/>

##### Bookmarking
The bookmarked section can be used to revisit annotations you are unsure about.

<img src="https://github.com/atharva-naik/XNLI-annotator/blob/main/images/bookmarking.png" width="800"/>

##### Annotation dashboard
1. Leaderboard: learn about the progress of your co-annotators, and how much progress you haved made. 
2. Label distribution and other statistics: Total number of annotators, how many annotations you have finished, inter-annotator agreement and pertinent dataset statistics are shown here. 
3. Export feature: export a jsonl file which is easy to read for both you and your computer (for processing and cleaning).

<img src="https://github.com/atharva-naik/XNLI-annotator/blob/main/images/dashboard_statistics.png" width="800"/>


<img src="https://github.com/atharva-naik/XNLI-annotator/blob/main/images/dashboard_annotations.png" width="800"/>