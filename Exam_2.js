const { request } = require('playwright');

async function testGithubOrgInfo(orgName = "SeleniumHQ") {
    const url = `https://api.github.com/orgs/${orgName}/repos`;
    let repos = [];
    let page = 1;

    const apiContext = await request.newContext({
        extraHTTPHeaders: {
            'User-Agent': 'playwright-api-testing'
        }
    });

    while (true) {
        let response = await apiContext.get(url, {
            params: {
                per_page: 100,
                page: page
            }
        });

        if (!response.ok()) {
            throw new Error(`HTTP error! status: ${response.status()}`);
        }
        
        let pageRepos = await response.json();
        if (!pageRepos || pageRepos.length === 0) {
            break;
        }
        repos.push(...pageRepos);
        page++;
    }

    if (repos.length === 0) {
        throw new Error(`Expected to find repositories for organization ${orgName}`);
    }
    console.log(`1. Total repositories found: ${repos.length}`);

    let totalOpenIssues = repos.reduce((sum, repo) => sum + (repo.open_issues_count || 0), 0);
    
    if (typeof totalOpenIssues !== 'number' || totalOpenIssues < 0) {
         throw new Error("Total open issues should be a non-negative integer");
    }
    console.log(`2. Total open issues across all repositories: ${totalOpenIssues}`);

    let sortedRepos = [...repos].sort((a, b) => {
        let valA = a.updated_at || '';
        let valB = b.updated_at || '';
        if (valA < valB) return 1;
        if (valA > valB) return -1;
        return 0;
    });

    if (sortedRepos.length > 1) {
        if (sortedRepos[0].updated_at < sortedRepos[sortedRepos.length - 1].updated_at) {
             throw new Error("Repositories should be sorted in descending order");
        }
    }

    console.log("3. Top 3 most recently updated repositories:");
    for (let i = 0; i < Math.min(3, sortedRepos.length); i++) {
        let r = sortedRepos[i];
        console.log(`   ${i + 1}. ${r.name} (Updated: ${r.updated_at})`);
    }

    let highestWatchersRepo = repos.reduce((maxRepo, repo) => {
        let rCount = repo.watchers_count || 0;
        let maxCount = maxRepo.watchers_count || 0;
        return rCount > maxCount ? repo : maxRepo;
    }, repos[0]);

    if (!highestWatchersRepo || !('name' in highestWatchersRepo) || highestWatchersRepo.watchers_count < 0) {
         throw new Error("Invalid highest watchers repository");
    }
    console.log(`4. Repository with the highest number of watchers: ${highestWatchersRepo.name} (${highestWatchersRepo.watchers_count} watchers)`);

    console.log("5. Running additional meaningful assertions...");
    let repoNames = repos.map(repo => repo.name.toLowerCase());
    let hasSelenium = repoNames.some(name => name.includes("selenium"));
    if (!hasSelenium) {
         throw new Error("Expected to find a repository with 'selenium' in the name");
    }

    for (let repo of repos) {
        if (!('updated_at' in repo) || typeof repo.updated_at !== 'string') {
             throw new Error(`Repository ${repo.name} missing updated_at`);
        }
    }

    console.log("All validations completed and passed successfully!");

    await apiContext.dispose();
}

if (require.main === module) {
    testGithubOrgInfo().catch(console.error);
}
