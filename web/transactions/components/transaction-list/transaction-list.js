import { useEffect, useState } from 'react';
import { ReloadOutlined } from '@ant-design/icons';
import { Button, Card } from 'antd';

import { DataGrid } from 'components/data-grid';
import Toolbar from 'components/toolbar';
import { LABELS } from 'components/i18n';
import { makeStore } from 'util/store';

import { TRANSACTIONS_GRID_STORE_ID } from './constants';
import { getAllTransactions } from './data';
import { buildColumns } from './grid/columnBuilder';

export function TransactionList() {
    const [transactions, setTransactions] = useState();
    const [reload, setReload] = useState(0);
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const [error, setError] = useState(null);

    const store = makeStore(TRANSACTIONS_GRID_STORE_ID);
    const columns = buildColumns(store);

    useEffect(() => {
        getAllTransactions().then(setTransactions).catch(setError);
    }, [reload]);

    function handleReload() {
        setReload(val => val + 1);
    }

    function handleSelectRow(selectedRows) {
        setSelectedRowKeys(selectedRows);
    }

    if (error) {
        return <Error error={error} />;
    }

    return (
        <Card bodyStyle={{ padding: 5 }}>
            <DataGrid
                dataSource={transactions}
                columns={columns}
                onSelectRow={handleSelectRow}
                store={store}
            >
                <Toolbar title={LABELS.transactionListGridTitle}>
                    <Button onClick={handleReload}>
                        <ReloadOutlined />
                    </Button>
                </Toolbar>
            </DataGrid>
        </Card>
    );
}
