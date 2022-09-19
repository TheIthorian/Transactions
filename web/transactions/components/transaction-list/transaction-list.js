import { useEffect, useState } from 'react';
import { Card } from 'antd';

import { useFilter } from 'hooks/filter';
import { DataGrid } from 'components/data-grid';
import { LABELS } from 'components/i18n';
import { Error } from 'components/error';
import { FilterToolbar } from 'components/filter-toolbar';

import { TRANSACTIONS_GRID_STORE_ID } from './constants';
import { getAllTransactions } from './data';
import { buildColumns } from './grid/columnBuilder';

export function TransactionList() {
    const {
        handleChangeTagFilter,
        handleChangeDateFrom,
        handleChangeDateTo,
        allTags,
        defaultSelectedTags,
        defaultDateFrom,
        defaultDateTo,
        filter,
        store,
    } = useFilter(TRANSACTIONS_GRID_STORE_ID);

    const [reload, setReload] = useState(false);
    const [transactions, setTransactions] = useState(null);
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const [error, setError] = useState(null);
    const [columns, setColumns] = useState([]);

    useEffect(() => {
        getAllTransactions(filter).then(setTransactions).catch(setError);
        setColumns(buildColumns({}));
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
        <Card style={{ marginTop: 10 }} bodyStyle={{ padding: 5 }}>
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
