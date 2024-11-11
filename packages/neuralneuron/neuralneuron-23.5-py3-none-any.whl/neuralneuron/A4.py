def a4():
    print('''

    mport networkx as nx
import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    """Fetch HTML content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_html(html_content):
    """Parse HTML content and extract links."""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()  # Use a set to avoid duplicates
    for a in soup.find_all('a', href=True):
        href = a['href']

        # Skip links that do not start with "http" to avoid relative URLs
        if href.startswith('http'):
            links.add(href)
    return links

def build_graph(urls):
    """Build a directed graph based on the links between the given URLs."""
    graph = nx.DiGraph()
    processed_urls = set()  # Track URLs that have been processed
    for url in urls:
        if url not in processed_urls:  # Process the URL only once
            html_content = fetch_html(url)
            if html_content:
                graph.add_node(url)  # Add the URL as a node (only once)
                processed_urls.add(url)  # Mark the URL as processed

                links = parse_html(html_content)
                for link in links:
                    if link not in processed_urls:  # Add edge only if the link is part of the provided URLs
                        graph.add_node(link)  # Ensure that the linked URL is also added as a node
                        graph.add_edge(url, link)  # Create a directed edge from URL to link
                        processed_urls.add(link)  # Mark the linked URL as processed
    return graph

def calculate_pagerank(graph):
    """Calculate PageRank for the nodes in the graph."""
    page_ranks = nx.pagerank(graph)
    return page_ranks

if _name_ == "_main_":
    # List of URLs to analyze (adjust the URLs as needed)
    urls_to_analyze = [
        'https://aws.amazon.com/what-is/data-science/#:~:text=Data%20science%20is%20the%20study,analyze%20large%20amounts%20of%20data.',
        'https://www.google.com/aclk?sa=l&ai=DChcSEwjS6YDq9ZyJAxUppWYCHSxtKcQYABACGgJzbQ&ae=2&aspm=1&co=1&ase=2&gclid=CjwKCAjw1NK4BhAwEiwAVUHPU',
        'https://www.ibm.com/topics/data-science',
        'https://www.udemy.com/?utm_source=aff-campaign&utm_medium=udemyads&LSNPUBID=50rqOrVy53Q&ranMID=47907&ranEAID=50rqOrVy53Q&ranSiteID=50rqOrVy53Q-UrGvfqa7HGPcTwKFJYV2_Q'
    ]

    # Step 1: Build the graph
    web_graph = build_graph(urls_to_analyze)

    # Step 2: Calculate the PageRank
    pagerank_values = calculate_pagerank(web_graph)

    # Step 3: Display the results
    print("PageRank Values:")
    for url, rank in pagerank_values.items():
        print(f"URL: {url}, PageRank: {rank:.4f}")

''')
a4()
