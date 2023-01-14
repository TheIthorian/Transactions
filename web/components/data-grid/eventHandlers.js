export function makeHandleTableChange(store) {
    return (pagination, filters, sorter) => {
        store.set('pagination', pagination);
        store.set('filters', filters);
        store.set('sorter', sorter);
    };
}
