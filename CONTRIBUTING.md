How We Work in This Repo
One shared repository, one branch per lane. Nobody forks.

Our decisions
Fill these in once the team agrees (see Step 0 of the README):

Corridor: Central Market (San Francisco)
Track: Micro-producer & supply continuity
Scenario: "We are a community lender in Central Market with $50,000 to invest in supply continuity. No one has applied for help. Here are the suppliers whose failure would hurt the most businesses downstream, and here is what we don't know."
Our test: When does the agent decline to fund the biggest hub? The most connected supplier is often the most robust, so the answer has to be in our demo.
Team lead:
Repo owner:
Lanes and branches
Lane	Branch	Owns
Data	data	Property graph, cascade query, edge weighting, equity audit
Agent	agent	ADK agent, prompts, custom tools, deployment (code lives in agent/)
Front end	frontend	The interface the demo runs on
Story	story	Deck, pitch video, Grant Memo, honest limitations
Everyone works in Cloud Shell. Keep your work inside the cloned repo, since only $HOME persists between sessions.

Daily workflow
# First time
git clone <repo-url>
cd <repo-name>
git checkout -b <your-lane>      # data, agent, frontend, or story

# Each session
git pull origin main             # bring in anything merged by others
git add .
git commit -m "Short, clear message"
git push -u origin <your-lane>
Merging into main
Open a pull request from your lane branch into main whenever you have something others need (a working query, a deployed endpoint, a mock response).

Merge early and often. Small, frequent merges beat one big merge at the end.

Tell the team in chat when you merge something they depend on.

If your branch conflicts with main:

git pull origin main
# fix the marked files, then:
git add .
git commit
git push
Handoffs to watch
Data → Agent: the property graph and a working cascade query. Hand this over early, because the agent lane is blocked without it.
Agent → Front end: a live endpoint. Deploy early, and until then the front end mocks the response.
Everyone → Story: which edges are real vs. modeled, the equity audit numbers, and what the agent can't do.
Shared project reminders
We share one Google Cloud project, so agree on who creates which tables or services before overwriting anything.
Don't commit secrets, keys, or credentials.
Everything we hand in goes through the submission portal: repo link, Skills project link, pitch deck, and pitch video.
