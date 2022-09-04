import { useState } from 'react';
import { PAGINATION } from './constants';

export function usePagination(store) {
    const pageSize = store?.get('pagination')?.pageSize || 10;
    const [paginationPage, setPaginationPage] = useState(store?.get('pagination')?.current || 1);
    return {
        ...PAGINATION,
        defaultPageSize: pageSize,
        current: paginationPage,
        onChange: setPaginationPage,
    };
}
