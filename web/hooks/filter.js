import { useEffect, useState } from 'react';
import moment from 'moment';

import { makeStore } from 'util/store';
import { API_URL, API_KEY } from 'config';
import { handleResponse } from 'util/rest';

async function getAllTags() {
    const response = await fetch(API_URL + '/getAllTags', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Api-Key': API_KEY,
            session_id: makeStore('user').get('session_id'),
        },
    });

    let data;
    try {
        data = await handleResponse(response);
    } catch {
        data = [];
    }
    return Array.from(new Set(data.map(t => t.l1)));
}

export function useFilter(storeId) {
    const store = makeStore(storeId);
    const [filter, setFilter] = useState({
        date_from: store.get('dateFrom'),
        date_to: store.get('dateTo'),
        tags: store.get('tagFilter')?.length
            ? {
                  l1: store.get('tagFilter'),
                  l2: store.get('l2TagFilter'),
                  l3: store.get('l3TagFilter'),
              }
            : {},
    });
    const [allTags, setAllTags] = useState([]);

    const dateFormat = 'YYYY-MM-DD';
    const defaultDateFrom = store.get('dateFrom')
        ? moment(store.get('dateFrom'), dateFormat)
        : undefined;
    const defaultDateTo = store.get('dateTo') ? moment(store.get('dateTo'), dateFormat) : undefined;
    const defaultSelectedTags = store.get('tagFilter');
    const defaultSelectedL2Tags = store.get('l2TagFilter');
    const defaultSelectedL3Tags = store.get('l3TagFilter');

    useEffect(() => {
        getAllTags().then(res => {
            setAllTags(res);
        });
    }, [filter]);

    function handleChangeTagFilter(values) {
        console.log('handleChangeTagFilter');
        store.set('tagFilter', values);
        if (values.length) {
            setFilter(filter => ({ ...filter, tags: { ...filter.tags, l1: values } }));
        } else {
            setFilter(filter => ({ ...filter, tags: { ...filter.tags, l1: [] } }));
        }
    }

    function handleChangeL2TagFilter(values) {
        console.log('handleChangeL2TagFilter');
        store.set('l2TagFilter', values);
        if (values.length) {
            setFilter(filter => ({ ...filter, tags: { ...filter.tags, l2: values } }));
        } else {
            setFilter(filter => ({ ...filter, tags: { ...filter.tags, l2: [] } }));
        }
    }

    function handleChangeL3TagFilter(values) {
        console.log('handleChangeL3TagFilter');
        store.set('l3TagFilter', values);
        if (values.length) {
            setFilter(filter => ({ ...filter, tags: { ...filter.tags, l3: values } }));
        } else {
            setFilter(filter => ({ ...filter, tags: { ...filter.tags, l3: [] } }));
        }
    }

    function handleChangeDateFrom(value) {
        console.log('handleChangeDateFrom');
        const date_from = value?.format('YYYY-MM-DD');
        store.set('dateFrom', date_from);
        setFilter(filter => ({ ...filter, date_from }));
    }

    function handleChangeDateTo(value) {
        console.log('handleChangeDateTo');
        const date_to = value?.format('YYYY-MM-DD');
        store.set('dateTo', date_to);
        setFilter(filter => ({ ...filter, date_to }));
    }

    return {
        handleChangeTagFilter,
        handleChangeL2TagFilter,
        handleChangeL3TagFilter,
        handleChangeDateFrom,
        handleChangeDateTo,
        allTags,
        defaultSelectedTags,
        defaultSelectedL2Tags,
        defaultSelectedL3Tags,
        defaultDateFrom,
        defaultDateTo,
        filter,
        store,
    };
}
