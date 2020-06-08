# Landing-Page-Tester
PLEASE COMMIT RESPONSIBLY
HOW TO UPLOAD YOUR SCRIPTS TO GITHUB
1. log in to your github account
2. Once you are logged in, go to the official repository https://github.com/OsasAzamegbe/Landing-Page-Tester
2.5 MAKE SURE YOU ARE ON THE "development" BRANCH.
3. Fork the repository ie Look for the fork icon in the top right and click it. If you are using a phone, make sure you are in "Desktop Mode"
4. You should now have a repository your_username/Landing-Page-Tester. 
5. clone the forked repo to your local machine and work on your feature separately
6. Commit your changes APROPRIATELY AS SEEN BELOW.
6.1. When you are done, go back and click "Create pull request".
6.5. Your pull request should be to "development" branch.

**IMPORTANT**
Best practice git/guthub flow by by the mentors of start.ng program
Here is the proposed git flow for teams:
You are expected to create a develop branch in addition to your default master branch.
For every feature, bug or chore, you must create a branch.
Example of a feature ?
User Login: Your branch name must follow this convention: feat/user-login (lower case and separated by dashes)
Example of a bug ?
Home Page Typo: Your branch naming: bug/homepage-typo
Example of a chore ?
Update Read Me: Your branch naming: chore/update-readme
Create a branch on your local git and only push to that branch. If you push to any other branch, you will be heavily penalized.
A typical way to do so:
run: git pull origin develop - You must pull from develop before or after checkout
git checkout -b feat/user-login - You are in the feat/user-login branch now
To push to github;
git add .
git commit -m "feat: implemented user login
git push origin feat/user-login - note how it ends with a branch.
on github, you must make a PR to the develop branch, any PR to the master branch must be closed with immediate alacrity.
When making a PR, your PR is expected to have the following:
What is the task completed ?
What the PR actually does  ?
How can this PR be manually tested ?
Any background contexts ? (maybe something a tester might not notice and be useful for testing)
Screenshots (of your implementation - a web page, a mobile app screen or an API payload
Your commit messages should follow a consistent pattern:
Remember, chore, feature, bug
So i do not want to see stuff like I tried my best in your commit messages;
For a feature: git commit -m "feat: implemented user log-in
For a bug: git commit -m "bug: fixed inconsistency in log in screen"
For a chore: git commit -m "chore: updated read me to include API endpoints"
Also, team leads, please set the develop branch as your default branch.
To prevent merge conflicts, Always pull from develop before making a PR
