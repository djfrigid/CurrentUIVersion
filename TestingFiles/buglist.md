# buglist

## Bugs:
- Provision for multiple source files
- Tag system
- extra field to questions, only for admins , triggers a deletion modal
- Make datasets downloadable # Issue with the storing of datasets, need to refine how they are stored to be able to pass the relevant data. <a href={% url 'download_dataset' dataset_id={{dataset %} class="btn btn-danger">Download</a>
- Fix the error with form data being provided, yet still returning a "field is required" error

## Current Action Item:

## For Later:
- Immediate viewing of best solution
- Fix questions page table styling
- General Styling Problems
- Confirmation of actions with modals, just little messages then the submit/cancel choice before it actually carries out the button function.
- Remove Logout from the logout page
- Add function decorators to restrict pages that need login to having been logged in.
- Account for failure and provide user feedback... everywhere
- Add a title block to generic_template, and then add titles to each page rather than just "JCoin" for everything.
- Rework login system to use django middleware
- Account Management Page

## Notes:
mongoimport -d JCoin -c polls_metadata --type csv --file D:\Python\Root\GroupProject\TestingFiles\Meta.csv --headerline

## Hours:

13
