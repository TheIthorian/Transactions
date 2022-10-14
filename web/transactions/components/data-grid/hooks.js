import { useState } from 'react';
import { PAGINATION, DEFAULT_PAGE_SIZE } from './constants';

export function usePagination(store) {
    const pageSize = store?.get('pagination')?.pageSize || DEFAULT_PAGE_SIZE;
    const [paginationPage, setPaginationPage] = useState(store?.get('pagination')?.current || 1);
    return {
        ...PAGINATION,
        defaultPageSize: pageSize,
        current: paginationPage,
        onChange: setPaginationPage,
    };
}
