from linkedin_scrapper import scrape_linkedin_posts

company_url = "https://www.linkedin.com/company/kalyna-group/"
posts = scrape_linkedin_posts(company_url)

if posts:
    for i, post in enumerate(posts, 1):
        print(f"🔹 Post {i}:\n{post}\n{'-'*40}")
else:
    print("No posts found.")