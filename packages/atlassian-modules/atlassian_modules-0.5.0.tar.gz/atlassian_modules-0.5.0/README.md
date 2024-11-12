The best way to interact with Atlassian Jira/Confluence API.

> **Note:** _This module is useful for the Atlassian Cloud_ <br>
> Your URL should look like this https://domain.atlassian.net


# Prerequisites
```python
from atlassian_modules import JiraHelper # for Jira
from atlassian_modules import  WikiHelper # for Wiki
```

# Getting Started

## Connectivity to Atlassian Jira

To initialize a connection to Jira, instantiate the `JiraHelper` class with your Jira URL, email, and API token:

```python
jira_helper = JiraHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)
```
______________________________________________________________________________
______________________________________________________________________________
# Atlassian Jira
______________________________________________________________________________
______________________________________________________________________________
## 1. Create a Jira Ticket

- You can create a new Jira ticket using the `create_ticket` method:

```python
jira_helper = JiraHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

ticket_url = jira_helper.create_ticket("PRJ", "Issue Summary", "Detailed issue description.", "Bug")
if ticket_url:
    print(f"Ticket created: {ticket_url}")
else:
    print("Failed to create ticket.")
```
Parameters:
- `project_key` (str): Key of the project where the new ticket will be created. This is usually a short, capitalized identifier for a project in JIRA. 
- `summary` (str): Summary of the new ticket. This is a concise overview of the issue or task. 
- `description` (str): Detailed description of the new ticket. This field is used to provide all necessary details about the issue or task. 
- `issue_type` (str): Type of the issue (e.g., `Bug`, `Task`, `Story`). This specifies what kind of ticket is being created.

Output:
- The function outputs informational messages about the process of creating a ticket, including preparing issue data, sending a request to create the ticket, and the result of that request.

Return:
- `URL of the created ticket (str)`: If the ticket creation is successful, the function returns the URL to access the newly created ticket directly. 
- `False`: If the ticket creation fails (for example, due to incorrect input parameters or server errors), the function returns `False`.
______________________________________________________________________________
## 2. Create a custom Jira Ticket
- You can create a new custom Jira ticket using the `create_custom_ticket` method:

```python
jira_helper = JiraHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

# Define additional fields if necessary
additional_fields = {
    "customfield_12345": "Custom value",
    "labels": ["label1", "label2"]
}

ticket_url = jira_helper.create_custom_ticket("PRJ", "Issue Summary", "Detailed issue description.", "Bug", additional_fields)
if ticket_url:
    print(f"Ticket created: {ticket_url}")
else:
    print("Failed to create ticket.")

```
Parameters:
- `project_key` (str): The key of the project where the new ticket will be created. This is typically a short, capitalized identifier specific to a project in Jira. 
- `summary` (str): A concise overview of the issue or task that the new ticket will represent. 
- `description` (str): A detailed description of the issue or task, providing all necessary details for understanding and addressing it. 
- `issue_type` (str): Specifies the type of issue being created (e.g., `Bug`, `Task`, `Story`), determining how the issue is categorized within Jira. 
- `additional_fields` (dict, optional): A dictionary of additional fields that are required for ticket creation. This parameter allows for the inclusion of project-specific or issue-specific information that is not covered by the standard fields.

Output:
- The function provides informational messages throughout the process of creating a ticket.
- These messages include details on preparing the issue data, sending a request to create the ticket, and the outcome of that request.
Return:
- `URL of the created ticket` (str): If the ticket creation is successful, the function returns the URL to access the newly created ticket directly. This allows for immediate navigation to the ticket for review or further action.
- `False`: If the ticket creation process fails, whether due to incorrect input parameters, server errors, or issues with the additional fields, the function returns `False`. This indicates that the ticket was not created and provides an opportunity to address any issues before retrying.
______________________________________________________________________________
## 3. Update the Jira ticket with inbuilt and custom fields
- You can update any custom field of Jira ticket using the `update_ticket_with_fields` method:
```python
jira_helper = JiraHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

# Define the additional fields you want to update
additional_fields = {
    "customfield_12345": "New custom value",
    "labels": ["newlabel1", "newlabel2"]
}

ticket_id = "PRJ-123"  # Example ticket ID to be updated

update_success = jira_helper.update_ticket_with_fields(ticket_id, additional_fields)
if update_success:
    print(f"Ticket {ticket_id} updated successfully.")
else:
    print(f"Failed to update ticket {ticket_id}.")
```
Parameters:
- `ticket_id` (str): ID (also known as the key) of the ticket to be updated. This identifier is typically a combination of the project key and a sequence number, like `PRJ-123`. 
- `additional_fields` (dict): A dictionary of fields to update the ticket with. This parameter allows specifying values for any standard or custom field in the ticket that supports updates.
Output:
- The function prints messages about the process of updating the ticket, including preparing the update data, making the request to update the ticket, and the result of that request.
Return:
- `True` if the update was successful. This indicates that the server accepted the update request and applied the changes to the ticket. 
- `False` otherwise. If the ticket update fails (for example, due to incorrect ticket ID, fields that cannot be updated, or server errors), the function returns `False`, and additional error information is printed to help diagnose the issue.
______________________________________________________________________________
## 3. Delete a Jira Ticket

- To delete a ticket, use the `delete_ticket` method:

```python
jira_helper = JiraHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

ticket_key = "PRJ-123"  # Example ticket key
if jira_helper.delete_ticket(ticket_key):
    print("Ticket deleted successfully.")
else:
    print("Failed to delete ticket or ticket does not exist.")
```
Parameters:
- `ticket_key` (str): The unique identifier for the ticket you wish to delete. This key is usually a combination of the project key and a number (e.g., "`PRJ-123`").

Output:
- The function itself does not print any output, but it performs a `DELETE` request to the JIRA REST API to delete the specified ticket.

Return:
- `True`: If the ticket is successfully deleted. This is indicated by a `204` HTTP status code from the JIRA API, meaning "`No Content`" but signifying successful deletion. 
- `False`: If the deletion fails, which can occur if the ticket does not exist or if there's an issue with the API request (e.g., permissions, invalid ticket key). This is communicated by returning `False`.
______________________________________________________________________________
## 4. Get Transition ID

```python
jira_helper = JiraHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

ticket_key = "PRJ-123"  # Example ticket key
transition_name = "Close"
transition_id = jira_helper.get_transitions(ticket_key, transition_name)
if transition_id:
    print(f"Transition ID for '{transition_name}' is {transition_id}.")
else:
    print(f"Transition '{transition_name}' not found for ticket {ticket_key} or failed to fetch transitions.")
```

Parameters:
- `ticket_key` (str): The key of the ticket for which transitions are being fetched. This is typically a unique identifier like "`PRJ-123`".
- `transition_to` (str): The name of the desired transition to look for. This is the human-readable name of the transition (e.g., "`Close`", "`Resolve`").

Output:
- The function prints messages about the process of fetching transitions for the ticket, including whether the transitions were successfully fetched, if the specific transition was found, and any errors encountered during the request.

Return:
- `Transition ID` (str): If the specified transition is found for the given ticket, the function returns the transition's ID, which can be used for further actions like transitioning the ticket to another status.
- `False`: If the specified transition is not found for the ticket, or if there is any failure in fetching transitions (e.g., due to an invalid ticket key, network issues, or server errors), the function returns `False`.
______________________________________________________________________________
## 5. Transition a Jira Ticket

- To transition a ticket to a different status, use the `transition_ticket` method:

```python
jira_helper = JiraHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

ticket_key = "PRJ-123"  # Example ticket key
transition_input = "Done"  # Can be a transition name like 'Done' or an ID like '31'
if jira_helper.transition_ticket(ticket_key, transition_input):
    print("Ticket transitioned successfully.")
else:
    print("Failed to transition ticket.")
```

Parameters:
- `ticket_key` (str): The key of the ticket you want to transition. This is a unique identifier for the ticket within JIRA. 
- `transition_input` (str or int): The desired transition for the ticket. This can be specified as either the name of the transition (e.g., "`Done`") or the transition ID (e.g., `31`).

Output:
- The function outputs informational messages regarding the transition process, including attempts to find the transition ID if a name is provided, and the result of the transition attempt.

Return:
- `True`: If the ticket transition is successful. This is indicated by a `204` HTTP status code, which means "`No Content`" but signifies that the operation completed successfully. 
- `False`: If the ticket transition fails. This could be due to various reasons, such as an invalid ticket key, an unrecognized transition name or ID, or a failure in the HTTP request itself.

______________________________________________________________________________
## 6. If exist a Jira Ticket

- To check if a ticket exist, use the `if_ticket_exist` method:

```python
jira_helper = JiraHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

ticket_key = "PRJ-123"  # Example ticket key
if jira_helper.if_ticket_exist(ticket_key):
    print("The ticket exists.")
else:
    print("The ticket does not exist.")
```
Parameters:
- `ticket_key` (str): The key of the ticket you want to check. This is a unique identifier for the ticket within JIRA.

Output:
- The function outputs messages that indicate whether it is checking for the existence of the specified ticket and the result of that check.

Return:
- `True`: If the ticket exists. This is confirmed by a `200` HTTP status code, indicating that the ticket was found. 
- `False`: If the ticket does not exist or if there was an error in checking. A `404` HTTP status code indicates the ticket does not exist. Other status codes indicate a failure in the request to check the ticket.
______________________________________________________________________________
## 7. Comment on a Jira ticket

- To comment on the ticket, use the `comment_ticket` method:

```python
jira_helper = JiraHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

ticket_key = "PRJ-123"  # Example ticket key
comment_text = "This is an example comment."
comment_url = jira_helper.comment_ticket(ticket_key, comment_text)
if comment_url:
    print(f"Comment added successfully: {comment_url}")
else:
    print("Failed to add comment to the ticket.")
```
Parameters:
- `ticket_key` (str): The key of the ticket to which you want to add a comment. This is a unique identifier for the ticket within JIRA. 
- `comment_text` (str): The text of the comment you wish to add to the ticket.

Output:
- The function outputs messages that indicate the process of adding a comment to the specified ticket, including checking if the ticket exists and attempting to add the comment.

Return:
- `URL of the created comment` (str): If adding the comment is successful, the function returns the URL to access the newly created comment directly. This is indicated by a `201` HTTP status code, meaning "`Created`". 
- `False`: If adding the comment fails. This could be because the ticket does not exist, the comment text is invalid, or there was an error in the request itself. In such cases, the function returns `False`.
______________________________________________________________________________
## 8. Pass the JQL and get the ticket array

- To query tickets using JQL, use the `jql_ticket` method:

```python
jira_helper = JiraHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

jql_query = "project = PRJ AND status = 'Open'"
max_results = 100  # Optional
ticket_keys = jira_helper.jql_ticket(jql_query, max_results)
if ticket_keys:
    print(f"Found tickets: {', '.join(ticket_keys)}")
else:
    print("Failed to retrieve tickets based on the JQL query.")
```

Parameters:
- `jql_query` (str): The Jira Query Language query string used to retrieve tickets. This string specifies the criteria that the returned tickets must meet.
- `max_results` (int, optional): The maximum number of tickets to retrieve. If not specified, the method attempts to fetch all tickets that match the query.

Output:
- The function outputs messages that detail the execution of the JQL query, including the number of tickets fetched in each batch and the total number of requested tickets.

Return:
- `List of ticket keys` (list): If successful, the function returns a list containing the keys of the tickets that match the JQL query criteria. Each key is a unique identifier for a ticket within JIRA.
- `False`: If the retrieval fails. This could be due to an issue with the JQL query, a problem with the request to JIRA, or if the JIRA server returns an unexpected status code. In such cases, the function returns `False`.
______________________________________________________________________________
## 9. Get the subject of a Jira Ticket

- To get the subject of a Jira ticket, use the `get_ticket_subject` method:

```python
jira_helper = JiraHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

ticket_key = "PRJ-123"  # Example ticket key
subject = jira_helper.get_ticket_subject(ticket_key)
if subject:
    print(f"Subject of the ticket: {subject}")
else:
    print("Failed to retrieve the subject of the ticket.")
```
Parameters:
- `ticket_key` (str): The key of the ticket for which you want to retrieve the subject. This is a unique identifier for the ticket within JIRA.

Output:  
- The function prints the subject of the specified ticket if it is successfully retrieved.

Return:
- Subject of the ticket (str): If the subject is successfully retrieved, the function returns the subject of the ticket.
- `False`: If the retrieval fails, the function returns False.
______________________________________________________________________________
______________________________________________________________________________
# Atlassian Wiki
______________________________________________________________________________
______________________________________________________________________________
## 1. Creating a wiki page
- To create wiki page, use the `create_wiki_page` method:
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

space_key = "DEV"
title = "API Documentation"
content = "<p>This is the API documentation for our project.</p>"
parent_page_id = 123456  # Optional
page_url = wiki_helper.create_wiki_page(space_key, title, content, parent_page_id)
if page_url:
    print(f"Wiki page created successfully: {page_url}")
else:
    print("Failed to create wiki page.")
```
Parameters:
- `space_key` (str): The key of the Confluence space where the new page will be created. Confluence spaces are containers for related content. 
- `title` (str): The title of the new page. Titles are used to identify pages within Confluence. 
- `content` (str): The content of the new page. This is usually HTML or Confluence storage format markup that defines the page's body. 
- `parent_page_id` (int, optional): The ID of a parent page if the new page is to be a child page. This parameter is optional; if not provided, the page will be created at the root of the specified space.

Output:
- The function outputs messages detailing the process of creating the Confluence page, including the attempt to create the page and the result of that attempt.

Return: 
- `URL of the created Confluence page` (str): If the page creation is successful, the function returns the URL to access the newly created page. This is indicated by a `200` HTTP status code. 
- `False`: If the page creation fails. This could be due to various issues, such as invalid input parameters, permissions problems, or server errors. In such cases, the function returns `False`.
______________________________________________________________________________
## 2. Duplicate a wiki page
- To duplicate wiki page, use the `duplicate_wiki_page` method:
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

source_page_id = "12345"  # Example source page ID
target_space_key = "TGT"  # Example target space key
target_title = "Duplicated Page Title"  # New title for the duplicated page
target_parent_page_id = "67890"  # Optional parent page ID for the new page

duplicated_page_url = wiki_helper.duplicate_wiki_page(source_page_id, target_space_key, target_title, target_parent_page_id)
if duplicated_page_url:
    print(f"Duplicated page successfully. View at: {duplicated_page_url}")
else:
    print("Failed to duplicate the page.")
```
Parameters:
- `source_page_id` (str): ID of the Confluence page you wish to duplicate. 
- `target_space_key` (str): Key of the Confluence space where the duplicated page will reside. 
- `target_title` (str): Title of the duplicated page. 
- `target_parent_page_id` (str, optional): ID of the parent page if the duplicated page is to be a child within the hierarchy. If not specified, the page will be created at the top level of the specified space.
Output:
- The method outputs messages detailing the process of duplicating a page, including fetching content from the source page and creating a new page with this content in the target space.

Return: 
- `URL of the duplicated Confluence page` (str): If the duplication is successful, the method returns the URL to access the newly created duplicated page. This URL is constructed from the response of the page creation process. 
- `None`: If the duplication fails at any point (e.g., retrieving content from the source page, creating the new page), the method returns `None`. This indicates that the operation was not successful, and no new page was created.
______________________________________________________________________________
## 3. Create a wiki page from template
- To create a wiki page from template use the `create_page_from_template` method:
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

template_id = "12345"  # Example template ID
space_key = "TGT"  # Example space key
title = "New Page from Template"  # Title for the new page
parent_page_id = "67890"  # Optional parent page ID

created_page_url = wiki_helper.create_page_from_template(template_id, space_key, title, parent_page_id)
if created_page_url:
    print(f"New page created successfully. View at: {created_page_url}")
else:
    print("Failed to create the new page from template.")
```
Parameters:
- `template_id` (str): ID of the Confluence template you wish to use for creating the new page. 
- `space_key` (str): Key of the Confluence space where the new page will be created. 
- `title` (str): Title of the new page. 
- `parent_page_id` (str, optional): ID of the parent page if the new page is to be a child within the space hierarchy. If not specified, the page will be created at the top level of the specified space.
Output:
- The function outputs messages that detail the process of creating a new page from a template, including checking for duplicate titles in the target space, retrieving content from the specified template, and the creation of the new page.
Return: 
- `URL of the created Confluence page` (str): If the page creation is successful, the function returns the URL to access the newly created page. This indicates that the page was created successfully and is accessible at the returned URL. 
- `None` or `False`: If the page creation fails, due to reasons such as template retrieval failure, duplicate title, or any error in the creation process, the function returns `None` or `False`. This indicates that no new page was created.
______________________________________________________________________________
## 4. Move wiki page from one location to another
- To move wiki page from one location to another location without changing title use `move_wiki_page` method:
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

page_id = "12345"  # Example page ID to be moved
target_space_key = "NEWSPACE"  # Target space key
target_position = "append"  # Position of the page relative to the parent page ('append', 'above', 'below')
target_parent_page_id = "67890"  # Optional new parent page ID

moved_page_url = wiki_helper.move_wiki_page(page_id, target_space_key, target_position, target_parent_page_id)
if moved_page_url:
    print(f"Page moved successfully. View at: {moved_page_url}")
else:
    print("Failed to move the page.")
```
Parameters:
- `page_id` (str): ID of the Confluence page you wish to move. 
- `target_space_key` (str): Key of the Confluence space where the page will be moved to. 
- `target_position` (str): Position to place the moved page relative to the parent page. Default is '`append`', but '`above`' and '`below`' are also valid options. 
- `target_parent_page_id` (str, optional): ID of the parent page if the moved page is to be nested under another page. If not specified, the page will be moved to the top level of the target space or as specified by `target_position`.
Output:
- The function outputs messages detailing the process of moving the page, including retrieving the current page title, preparing the move operation, and executing the move.
Return: 
- `URL of the moved Confluence page` (str): If the move operation is successful, the function returns the URL to access the moved page. This indicates that the page was successfully moved to the new space and position. 
- `None` or `False`: If the move operation fails, due to reasons such as an error retrieving the current page details, an error in the move operation, or inability to retrieve the moved page URL, the function returns `None` or `False`. This indicates that the page was not successfully moved.
______________________________________________________________________________
## 5. Check if wiki page exist
- To move wiki page from one location to another location without changing title use `move_wiki_page` method:
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

title = "Example Page Title"  # Title of the Confluence wiki page to check
space_key = "EX"  # Key of the Confluence space

if wiki_helper.wiki_page_exists(title, space_key):
    print(f"The page '{title}' exists in space '{space_key}'.")
else:
    print(f"The page '{title}' does not exist in space '{space_key}'.")
```
Parameters:
- `title` (str): Title of the Confluence wiki page to check for existence. 
- `space_key` (str): Key of the Confluence space where the page might reside.
Output:
- The function outputs a message indicating the start of the check process and then reports whether the specified page exists in the given space based on the title.
Return: 
- `True`: If the page exists. This is determined by the presence of results matching the specified title in the specified space. 
- `False`: If the page does not exist or if there was an error during the request. This could be due to the specified page not being found in the given space or an issue with the Confluence API response.
______________________________________________________________________________
## 6. Retrieve all child pages
- Recursively retrieve all descendant pages of a given parent page ID.
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

parent_id = "12345"  # Example parent page ID
child_pages = wiki_helper.get_child_pages_recursive(parent_id)
if child_pages:
    print("Child pages found:")
    for page in child_pages:
        print(f"Title: {page['title']}, ID: {page['id']}, Parent ID: {page['parentid']}")
else:
    print("No child pages found or failed to fetch.")
```
Parameters:
- `parent_id` (str): ID of the parent Confluence wiki page from which to start retrieving descendant pages.
Output:
- The method does not directly print any output but provides a mechanism for recursively fetching and listing all child pages beneath a given parent page. It operates by:
  - Fetching the direct children of the provided parent ID. 
  - Recursively calling itself for each child to fetch further descendants, accumulating all pages in a list. 

Return: 
- `List of child pages`: Returns a list of dictionaries, each containing the title, ID, and parent ID of each descendant page found. This allows for a comprehensive view of the hierarchy and content under the specified parent page. 
- If the retrieval fails at any point (due to an error in fetching child pages, for instance), the recursive fetching process is designed to continue for other branches of the tree, aiming to return as complete a list as possible of descendant pages.
______________________________________________________________________________
## 7. Get wiki page ID
- Retrieve the ID of a Confluence wiki page by its title.
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

title = "Example Page"  # Title of the Confluence wiki page to search for
space_key = "EX"  # Key of the Confluence space

page_id = wiki_helper.get_page_id(title, space_key)
if page_id:
    print(f"Found page '{title}' with ID: {page_id} in space '{space_key}'.")
else:
    print(f"No page found with the title '{title}' in space '{space_key}'.")
```
Parameters:
- `title` (str): Title of the Confluence wiki page you're looking for. 
- `space_key` (str): Key of the Confluence space where you're searching for the page.
Output:
- The function outputs a message indicating the process of searching for the page by its title within the specified space and then reports the outcome of the search:
  - If a page with the specified title exists in the given space, it prints the page ID and confirms the page was found. 
  - If no page with the specified title exists in the given space, it indicates no page was found. 
  - If there's an error in the search process (e.g., issues with the Confluence API response), it reports the failure.

Return:
- `ID of the page` (str): If a page with the specified title is found in the given space, the function returns the ID of the page. 
- `False`: If no page is found with the given title in the specified space, or if there was an error during the request, the function returns `False`.
______________________________________________________________________________
## 8. Replace word in wiki
- Replace all occurrences of a string in a Confluence wiki page.
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

page_id = "123456"  # Example page ID
from_string = "old text"  # Text to be replaced
to_string = "new text"  # Replacement text

if wiki_helper.replace_in_page(page_id, from_string, to_string):
    print(f"Replaced all occurrences of '{from_string}' with '{to_string}' in page ID: {page_id}.")
else:
    print("Failed to replace text in the page.")
```
Parameters:
- `page_id` (str): ID of the Confluence wiki page where the replacement will be made. 
- `from_string` (str): The string to be replaced in the page's content. 
- `to_string` (str): The string to use as a replacement.
Output:
- The function outputs messages detailing the process of fetching the page content, performing the replacement, and updating the page with the new content:
  - It starts by fetching the current content and version number of the specified page. 
  - It then replaces all occurrences of the `from_string` with the `to_string` within the page's content.
  - If replacements are made, it updates the page with the new content and increments the version number. If no occurrences are found, it indicates so and considers the operation successful without making an update.

Return:
- `True`: If the replacement operation was successful, whether replacements were made or not (including the case where the `from_string` was not found). 
- `False`: If there was a failure at any point during the process, such as an error fetching the page content, or updating the page with the new content.
______________________________________________________________________________
## 9. Fetch tables from wiki
- Fetch all tables from a Confluence wiki page.
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

page_id = "123456"  # Example page ID

tables_json = wiki_helper.get_tables_from_page(page_id)
if tables_json:
    print("Found tables on the page:")
    print(tables_json)
else:
    print("Failed to fetch tables or no tables found on the page.")
```
Parameter
- `page_id` (str): ID of the Confluence wiki page from which to fetch tables.

Output:
- The function initiates by fetching the content of the specified Confluence wiki page. It then parses the HTML content of the page to find and extract data from all tables present on the page. Each table's data is converted into a JSON structure, providing an easy-to-read format of the tables' contents.
Return:
- JSON structure: Returns a JSON string that represents all the tables found on the page. Each table is structured into a JSON object with keys representing the table headers and values representing the row data. If multiple tables are found, they are indexed as `table1`, `table2`, etc., in the JSON structure. 
- If the fetching fails (due to an unsuccessful API call) or if no tables are found on the page, the function returns an empty JSON object (`{}`).
______________________________________________________________________________
## 10. Replace the whole wiki page
- Replace the entire Confluence wiki page with the new content
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

page_id = "12345"  # Example page ID
new_content = "<p>This is the new content for the page.</p>"  # HTML content

if wiki_helper.update_wiki_page(page_id, new_content):
    print(f"Page ID: {page_id} was updated successfully.")
else:
    print(f"Failed to update the page ID: {page_id}.")
```
Parameter
- `page_id` (str): The ID of the Confluence wiki page that you want to update. 
- `new_content` (str): The new content to replace the existing content of the page. This content is typically in `HTML` format.

Output:
- The method prints messages to inform the user about the process steps, including fetching current page data and attempting to update the page with new content.
Return:
- `True`: If the page content update is successful. This is indicated by a status code of `200` from the Confluence REST API, showing that the update request was processed correctly. 
- `False`: If the update fails. This could be due to various reasons such as an invalid page ID, issues with the Confluence server, or improper formatting of the new content. Failure is indicated by any status code other than `200`, and the method prints the error details received from the server.
______________________________________________________________________________
## 11. Get parent page ID
- Retrieve the parent ID of a Confluence wiki page by passed page ID.
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

page_id = "123456"  # Example page ID

parent_id = wiki_helper.get_parent_page_id(page_id)
if parent_id:
    print(f"Parent page ID for page ID {page_id}: {parent_id}")
else:
    print(f"No parent page found for page ID {page_id}, or failed to fetch.")
```
Parameter
- `page_id` (str): The ID of the Confluence wiki page for which you want to find the parent page.

Output:
- The method outputs a message indicating it is fetching the parent page ID for the specified page. It then either reports the ID of the parent page, states that no parent page was found, or indicates a failure to fetch the parent page ID.

Return:
- `ID of the parent page` (str): If the specified page has a parent page, the method returns the ID of the parent page. This is useful for understanding the hierarchy of pages within Confluence spaces. 
- `False`: If no parent page exists for the specified page or if there was an error in the fetch operation (such as an invalid page ID or a problem with the Confluence server), the method returns False. This helps to identify pages that are at the top level of their space or when an issue occurs with the retrieval process.
______________________________________________________________________________
## 12. Add Table of Content (TOC) in wiki page
- Add a Table of Contents (TOC) to a Confluence wiki page if it doesn't already have one.
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

page_id = "123456"  # Example page ID

result_message = wiki_helper.add_toc_to_page(page_id)
print(result_message)
```
Parameter
- `page_id` (str): The ID of the Confluence wiki page where you want to add a Table of Contents.

Output and Return
- The function returns a **message** indicating the operation's result. This could be a confirmation that the TOC was added successfully, a message stating that the TOC already exists, or an error message if the operation failed. 
- **Error Handling**: If there are issues fetching the page data or updating the page, the function provides detailed error messages including the status code and response text from Confluence's API. This is helpful for diagnosing problems with the operation.
______________________________________________________________________________
## 13. Add row to the existing table in wiki page (beta)
- Pass the header to identify the table and then add the row to that identified table
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)
page_id = "123456"  # Example page ID
headers = ["Header1", "Header2", "Header3"]  # The headers of the table you're targeting
row_data = ["Data1", "Data2", "Data3"]  # The data for the new row

result_message = wiki_helper.add_row_to_table(page_id, headers, row_data)
print(result_message)
```
Parameters 
- `page_id` (str): The ID of the Confluence page you're modifying. 
- `headers` (list of str): A list of headers representing the columns of the table. This ensures that the data is added to the correct column. 
- `row_data` (list of str): A list of values corresponding to each header, forming the new row.

Output and Return
- The function returns a message indicating the result of the operation. This could be a confirmation of successful row addition, or an error message detailing why the operation failed.

______________________________________________________________________________
## 14. Add/Update row to the existing table in wiki page (beta)
- Pass the header to identify the table and then add/update the row to that identified table
```python
wiki_helper = WikiHelper(ATLASSIAN_URL, EMAIL, API_TOKEN)

page_id = "123456"  # Example page ID
headers = ["Cluster Name", "Component Name", "Next Version"]  # The headers of your table
new_row_data = ["Cluster1", "ComponentA", "v2.0"]  # Data for the new or updated row

result_message = wiki_helper.update_or_add_table_row(page_id, headers, new_row_data)
print(result_message)
```
Parameter
- `page_id` (str): The ID of the Confluence page containing the table. 
- `headers` (list of str): A list of headers representing the columns of the table. It's crucial for identifying the correct columns when updating or adding rows. 
- `new_row_data` (list of str): The values for the new or updated row, aligned with the headers order.
Output and Return
- The function returns a message indicating the result of the operation, such as successful row update, successful addition of a new row, or an error if the operation failed.
______________________________________________________________________________
# Data Privacy Note

🔒 **We respect your privacy**: This module does **not** store any of your data anywhere. It simply interacts with the Atlassian Jira API to perform the requested operations. Ensure you manage your connection details securely.

# Release Notes

## Latest Release: 0.5 (11 Nov 2024)
- New Features:
  - Added `get_ticket_subject` function to `JiraHelper` class for retrieving the subject of a Jira ticket by its ID.
- Beta Features (Continued from previous release):
  - Beta functions `wiki_helper.add_row_to_table` & `wiki_helper.update_or_add_table_row` for improved table management.
- Minor documentation updates for clarity and consistency.

## Previous Releases:
- 0.4.1 (28 May 2024)
- Revision in documentation for better understanding
  - Based on the internal design now `JIRA_URL`, `CONFLUENCE_URL` is replaced with `ATLASSIAN_URL`
  - Technically we are using `https://domain.atlassian.net` only to address Jira and Wiki both
  - This is mentioned in the top of the document as well
- Beta Features (Continued from previous release):
  - Beta functions `wiki_helper.add_row_to_table` & `wiki_helper.update_or_add_table_row` for improved table management.
- 0.4 (21 Mar 2024)
- New Features:
  - JIRA Integration Enhancements:
    - Custom Ticket Creation: The `create_custom_ticket` function has been introduced, allowing for more flexible ticket creation in JIRA projects. This function supports additional fields, enabling users to specify custom data during ticket creation. 
    - Ticket Field Updates: The `update_ticket_with_fields` method has been added, offering the ability to update existing tickets with new or modified fields. This feature is crucial for maintaining accurate and up-to-date ticket information.
- Beta Features (Continued from previous release):
  - Beta functions `wiki_helper.add_row_to_table` & `wiki_helper.update_or_add_table_row` for improved table management.
- 0.3 (21 Mar 2024)
  - Enhancements:
    - Updated `readme.md` documentation. 
    - Introduced beta functions `wiki_helper.add_row_to_table` & `wiki_helper.update_or_add_table_row` for improved table management.
- 0.2.8 (21 Mar 2024)
  - Minor updates and enhancements (details forthcoming).
- 0.2.7 (08 Jan 2024)
  - New Features:
    - `add_toc_to_page`: Automatically adds a table of contents to wiki pages lacking one. 
  - Documentation:
    - Updated `README.md` with guidance on using `add_toc_to_page`.
- 0.2.6 (05 Jan 2024)
  - New Features:
    - `get_parent_page_id`: Retrieves the parent ID for a given wiki page ID. 
  - Documentation:
    - Updated `README.md` with instructions for `get_parent_page_id`.
- 0.2.5.4 (04 Jan 2024)
  - New Features:
    - `update_wiki_page`: Replaces entire wiki page content with new content.
  - Documentation:
    - Updated `README.md` with usage information for `update_wiki_page`.
- 0.2.5.3 (04 Jan 2024)
  - Internal testing release; not intended for general use.
- 0.2.5.2 - 0.2.5 (04 Jan 2024)
  - Withdrawn due to potential bugs.
- 0.2.4 (13 Oct 2023)
  - New Features:
    - `get_tables_from_page`: Fetches all tables from a wiki page in JSON format, simplifying table extraction. 
  - Documentation:
    - Updated `README.md` with `get_tables_from_page` usage details.
- 0.2.3.1 (21 Sep 2023)
  - Documentation:
    - Updated `README.md` with usage information for `get_page_id` and `replace_in_page`.
- 0.2.3 (21 Sep 2023)
  - Confluence Integration:
    - Added `get_page_id` to retrieve wiki page IDs.
- 0.2.2.1 (21 Sep 2023)
  - Performance improvements and extra output suppression. 
  - Confluence Integration:
    - Added `replace_in_page` for in-page text replacement.
- 0.2.2 (20 Sep 2023)
  - Documentation:
    - Enhanced `README.md` for better clarity. 
  - Confluence Integration:
    - Added `get_child_pages_recursive` to fetch child pages recursively.
- 0.2.1 (20 Sep 2023) - Major Release 
  - Enhancements:
    - Comprehensive `README.md` update for improved understanding. 
    - Fine-tuned output monitoring and improved return format. 
  - Confluence Integration:
    - Multiple functionalities added, including page creation, duplication, template usage, moving pages, and existence checks.
- 0.2 (20 Sep 2023)
  - Withdrawn due to potential bugs.
- 0.1.4.1 (18 Sep 2023)
  - Documentation:
    - Updated `README.md` for enhanced understanding. 
- 0.1.4 (18 Sep 2023)
  - Improvements:
    - Suppressed extraneous output for cleaner integration.
    - Detailed function outputs in `README.md`. 
  - Features:
    - Added Jira ticket search, commenting, and JQL processing functions. 
- 0.1.3 (18 Sep 2023)
  - Withdrawn due to potential bugs. 
- 0.1.2.1 (16 Sep 2023)
  - Documentation:
    - Reformatted `README.md`. 
- 0.1.2 (16 Sep 2023)
  - Features:
    - Added `if_exist_ticket` for Jira ticket existence checks.
  - Documentation:
    - Updated `README.md` format.
- 0.1.1 (16 Sep 2023)
  - Features:
    - Added `transition_ticket` for Jira ticket transitions, with ID flexibility.
  - Documentation:
    - Clarified module usage in `README.md`.
- 0.1 (16 Sep 2023)
  - Initial Release:
    - Introduced Jira ticket management functions: `create`, `delete`, and `transition tickets`.