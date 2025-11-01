from duckduckgo_search import DDGS

def search_destination(destination, duration, interests):
    ddgs = DDGS()
    try:
        search_queries = [
            f"best things to do in {destination} travel guide",
            f"{destination} attractions landmarks tourism",
            f"{destination} local culture customs"
        ]
        
        for interest in interests:
            search_queries.append(f"{destination} {interest} activities")
        
        all_results = []
        for query in search_queries:
            try:
                results = list(ddgs.text(query, max_results=3))
                all_results.extend(results)
            except Exception:
                continue
        
        combined_info = []
        for result in all_results[:10]:
            if result.get('title') and result.get('body'):
                combined_info.append(f"Title: {result['title']}\nDescription: {result['body']}\n")
        
        return "\n".join(combined_info) if combined_info else f"Basic information about {destination}: A popular travel destination."
        
    except Exception:
        return f"Search completed with some limitations. Proceeding with available information about {destination}."