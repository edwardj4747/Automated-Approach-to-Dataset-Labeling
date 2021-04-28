This is the code for looking for explicit datasets in the references (and text)
sections of the papers. It also looks for free text in the reference section that
does not have a doi or a short name but makes has the words 'GES DISC' or a link
to the the GES DISC website.

The current process is as follows (if you have an idea to improve it, you are 
more than welcome to change it):
* To find the explicit citations
    1) Run `explicit_references.py`. This generates a dictionary keyed based
    on the PDF key and with the explicit DOIs found, Short Names found, and 
    free text citations found
    2) Run `split_references.py`. This cleans up the free text citations and
    removes a lot of extra references
    3) Run `improve_doi_matching.py` to pick up a few more dois that were 
    originally in the free text, and update the doi and free text  fields 
    accordingly.
* To input in Zotero
    1) sources: `write_sources_to_zotero.py`. Add the 'source:xxx xxxx' tags to
    Zotero based on features that were extracted
    2) datasets and DOIs: `create_zotero_csv.py` then `write_citations_to_zotero.py`.
    This adds the 'reviewer:autolabel' tag as well as the 'doi:xxxx' tags and
    the notes with the Short Names and a 'category:unknown' tag.
    

As always, the indiviaul code files have more comments.

