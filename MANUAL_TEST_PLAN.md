# Resume to Rank Manual Test Plan

## Summary

This manual test plan validates the Resume to Rank application from the perspective of a hiring manager. The plan is human-executable, high-level, and limited to manual QA only. It does not include code, automation scripts, or implementation details.

## Test Coverage

- Ranking table generation based on selected hiring criteria.
- Regenerating or updating an existing ranking table.
- Drag-and-drop resume upload for logged-in hiring managers.
- Resume privacy and access restriction for unauthorized or logged-out users.
- Candidate list display after uploads.
- Sorting candidates by selected top skills.
- Usability of sorting and ranking with longer candidate lists.

## Assumptions

- Testers have access to hiring manager accounts and at least one unauthorized or logged-out session.
- Sample resumes are available for upload and ranking.
- Candidate skill information is available after resume upload.
- Privacy validation focuses on application-level access behavior visible to a manual tester.

## Checklist

- [ ] TC-01: Generate a ranking table based on selected criteria
  - Prerequisites: Hiring manager is logged in; multiple candidate resumes are available in the app; ranking criteria options are available.
  - Steps:
    1. Navigate to the resume ranking workflow.
    2. Select one or more ranking criteria.
    3. Start the ranking process.
    4. Wait for the ranking table to appear.
    5. Review the candidates shown in the table.
  - Expected: A ranking table is generated using the selected criteria and includes the uploaded candidates.
  - Criteria: Passes if the table appears, candidates are ranked, and the ranking reflects the criteria selected by the hiring manager.

- [ ] TC-02: Generate a new ranking table when one already exists
  - Prerequisites: Hiring manager is logged in; resumes have been uploaded; a ranking table has already been generated.
  - Steps:
    1. Open the existing ranking table.
    2. Change the selected ranking criteria.
    3. Generate or refresh the ranking table.
    4. Compare the updated table to the prior result.
  - Expected: The app updates or replaces the ranking table based on the newly selected criteria.
  - Criteria: Passes if the table reflects the new criteria and does not incorrectly preserve outdated ranking results.

- [ ] TC-03: Access resume upload as a logged-in hiring manager
  - Prerequisites: Hiring manager account exists and can log in.
  - Steps:
    1. Log in as a hiring manager.
    2. Navigate to the resume upload page.
    3. Confirm the upload area is visible.
  - Expected: The logged-in hiring manager can access the resume upload page.
  - Criteria: Passes if the upload page loads successfully and provides a clear resume upload area.

- [ ] TC-04: Drag and drop resumes into the upload area
  - Prerequisites: Hiring manager is logged in; resume upload page is open; one or more resume files are available locally.
  - Steps:
    1. Drag one resume file into the upload area.
    2. Confirm the app acknowledges the file.
    3. Drag multiple resume files into the upload area.
    4. Confirm the app acknowledges all accepted files.
    5. Complete the upload action if required.
  - Expected: The app accepts dragged resume files and makes them available for ranking.
  - Criteria: Passes if uploaded resumes appear in the app and can be used in the candidate ranking workflow.

- [ ] TC-05: Restrict resume access to authorized users
  - Prerequisites: At least one resume is stored in the system; one authorized hiring manager account exists; one unauthorized user account or logged-out session is available.
  - Steps:
    1. Log in as an authorized hiring manager.
    2. Confirm stored resumes are accessible.
    3. Log out.
    4. Attempt to access the same resumes while logged out.
    5. Log in as an unauthorized user.
    6. Attempt to access the same resumes.
  - Expected: Only authorized users can access stored resumes.
  - Criteria: Passes if authorized users can view permitted resumes and unauthorized or logged-out users cannot.

- [ ] TC-06: Verify stored resumes remain private
  - Prerequisites: Resumes are stored in the system; at least two user accounts with different access permissions are available.
  - Steps:
    1. Log in as a hiring manager who uploaded or owns a set of resumes.
    2. Confirm those resumes are visible.
    3. Log out.
    4. Log in as a different user who should not have access to those resumes.
    5. Check whether the original resumes are visible or accessible.
  - Expected: Stored resumes are only visible to users with appropriate authorization.
  - Criteria: Passes if users cannot view, open, rank, or otherwise access resumes they are not authorized to use.

- [ ] TC-07: Verify privacy during normal logged-in use
  - Prerequisites: Hiring manager is logged in; resumes are uploaded; candidate data is visible in the app.
  - Steps:
    1. Navigate through the upload, candidate list, and ranking table views.
    2. Confirm resume information is shown only within authenticated app pages.
    3. Log out.
    4. Use browser navigation or direct access attempts to return to resume-related pages.
  - Expected: Resume data is not accessible after logout.
  - Criteria: Passes if resume-related pages require authentication and do not expose private candidate information after logout.

- [ ] TC-08: Display candidate list after uploading resumes
  - Prerequisites: Hiring manager is logged in; multiple resumes have been uploaded successfully.
  - Steps:
    1. Navigate to the candidate list view.
    2. Confirm uploaded candidates are displayed.
    3. Review candidate names or identifiers.
    4. Confirm relevant skill information is shown where applicable.
  - Expected: The uploaded candidates appear in a candidate list.
  - Criteria: Passes if all uploaded candidates are represented and the list is usable for review and sorting.

- [ ] TC-09: Sort candidates by a selected top skill
  - Prerequisites: Candidate list is displayed; candidates have skill information available; at least one top skill can be selected.
  - Steps:
    1. Select a top skill to sort by.
    2. Apply the sort.
    3. Review the order of candidates.
  - Expected: Candidates are sorted according to the selected skill.
  - Criteria: Passes if candidates with stronger or more relevant matches for the selected skill appear higher than candidates with weaker or missing matches.

- [ ] TC-10: Change sorting from one skill to another
  - Prerequisites: Candidate list is displayed; multiple sortable skills are available.
  - Steps:
    1. Sort candidates by one skill.
    2. Observe the resulting order.
    3. Select a different skill.
    4. Apply the new sort.
    5. Observe the updated order.
  - Expected: The candidate list updates to reflect the newly selected skill.
  - Criteria: Passes if the ordering changes appropriately and the previous sort does not incorrectly remain active.

- [ ] TC-11: Sort candidates when some candidates do not match the selected skill
  - Prerequisites: Candidate list is displayed; at least one candidate matches the selected skill and at least one candidate does not.
  - Steps:
    1. Select a top skill that only some candidates have.
    2. Apply the sort.
    3. Review placement of matching and non-matching candidates.
  - Expected: Candidates matching the selected skill are prioritized over candidates without that skill.
  - Criteria: Passes if matching candidates are easy to identify and appear ahead of non-matching candidates according to the app's ranking behavior.

- [ ] TC-12: Confirm ranking and sorting remain usable with a longer candidate list
  - Prerequisites: Hiring manager is logged in; enough resumes have been uploaded to create a long candidate list.
  - Steps:
    1. Open the candidate list.
    2. Select one or more top skills.
    3. Sort the candidate list.
    4. Generate or view the ranking table.
    5. Review whether the list remains understandable and navigable.
  - Expected: The app supports reviewing and sorting a longer list of candidates.
  - Criteria: Passes if the hiring manager can sort, review, and compare candidates without losing access to key candidate information.
