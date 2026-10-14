# Tasks for your LOCAL Claude (PowerShell window, with /chrome enabled)

First, in PowerShell inside the `research-` folder, get the latest files:
```
git pull
```
Then start Claude with `claude --continue` and paste ONE task at a time.

---

## Task A: Email tracker in Google Sheets
```
Open Google Sheets in my Chrome (signed in as askedfirst.audits@gmail.com), create a new sheet called "AskedFirst Outreach Tracker", and fill it with the contents of geo-dentists/outreach/charlotte-nc/tracker.csv. Then check my Gmail Sent folder and, for each practice I already emailed, fill in the email/contact used and the date sent. Freeze the header row. Don't send or delete anything.
```

## Task B: Follow-up drafts (run on day 4-5 after the first emails)
```
Check my Gmail (askedfirst.audits@gmail.com). For each Charlotte practice I emailed 4 or more days ago that has NOT replied, create a draft reply in the same email thread using the text in geo-dentists/outreach/charlotte-nc/followups/<practice>.md (Follow-up 1 only). Keep [MY MAILING ADDRESS] as a placeholder. Do not send. Then update the tracker sheet's "Follow-up 1 sent" column with "draft ready".
```

## Task C: Put the website online (Netlify + Formspree)
```
Help me publish geo-dentists/landing-page/index.html for free:
1. In Chrome, open formspree.io, and help me sign up with askedfirst.audits@gmail.com (I'll type the password myself). Create a form named "AskedFirst free check" and get its form ID.
2. Replace YOUR_FORM_ID in geo-dentists/landing-page/index.html with that ID, and commit.
3. Open app.netlify.com/drop, help me sign up with askedfirst.audits@gmail.com, then tell me exactly which folder to drag in (geo-dentists/landing-page). After it deploys, rename the site to "askedfirst" (or the closest available name) in Site settings.
4. Open the live site, submit a test signup, and confirm it arrives in Gmail.
Stop and ask me before entering any password or payment details.
```

## Task D: LinkedIn profile
```
I'm logged in to LinkedIn in Chrome. Using geo-dentists/outreach/linkedin-profile.md, fill in my profile: headline, location, About section, an Experience entry (Founder, AskedFirst, Oct 2026 – present), and the 5 skills. Show me each section before saving it. Don't post anything, don't send connection requests, and don't change my name or photo.
```

After Task C is done, ask Claude to add the website link to LinkedIn's Featured section and to your Gmail signature.
