import { useEffect, useState } from 'react';
import { Card } from 'antd';

import { useFilter } from 'hooks/filter';
import { DataGrid } from 'components/data-grid';
import { LABELS } from 'components/i18n';
import { Error } from 'components/error';
import { FilterToolbar } from 'components/filter-toolbar';
import { makeStore } from 'util/store';

import { TRANSACTIONS_GRID_STORE_ID } from './constants';
import { getAllTransactions } from './data';
import { buildColumns } from './grid/columnBuilder';

export function TransactionList() {
    const [transactions, setTransactions] = useState();
    const [reload, setReload] = useState(false);
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const [error, setError] = useState(null);

    const {
        handleChangeTagFilter,
        handleChangeDateFrom,
        handleChangeDateTo,
        allTags,
        defaultSelectedTags,
        defaultDateFrom,
        defaultDateTo,
        filter,
    } = useFilter(TRANSACTIONS_GRID_STORE_ID);

    const store = makeStore(TRANSACTIONS_GRID_STORE_ID);
    const columns = buildColumns(store);

    useEffect(() => {
        getAllTransactions(filter).then(setTransactions).catch(setError);
    }, [filter, reload]);

    function handleReload() {
        setReload(reload => !reload);
    }

    function handleSelectRow(selectedRows) {
        setSelectedRowKeys(selectedRows);
    }

    if (error) {
        return <Error error={error} />;
    }

    return (
        <Card bodyStyle={{ padding: 5, marginTop: 10 }}>
            <DataGrid
                dataSource={transactions}
                columns={columns}
                onSelectRow={handleSelectRow}
                store={store}
            >
                <FilterToolbar
                    title={LABELS.transactionListGridTitle}
                    {...{
                        handleChangeTagFilter,
                        handleChangeDateFrom,
                        handleChangeDateTo,
                        allTags,
                        defaultSelectedTags,
                        defaultDateFrom,
                        defaultDateTo,
                        handleReload,
                    }}
                ></FilterToolbar>
            </DataGrid>
        </Card>
    );
}
