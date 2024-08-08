
def get_pagination_serialization(pagination,sort,sort_order):
    data = {}
    if pagination:
         data['page_size'] = pagination.page_size
         data['page_number'] = pagination.page_number
         data['num_pages'] = pagination.num_pages
         data['total_results'] = pagination.total_results
    if sort:
        data['sort'] = sort
    if sort_order:
        data['sort_order'] = sort_order
    return data
