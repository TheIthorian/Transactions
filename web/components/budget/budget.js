import { ReloadOutlined } from '@ant-design/icons';
import { Button, Divider, Skeleton } from 'antd';
import { useEffect, useState } from 'react';
import { BudgetItem } from './budget-item';
import { getBudget, getBudgetItems } from './data';

export default function Budget({ budgetId, name, totalLimit }) {
    const [loading, setLoading] = useState(true);
    const [reload, setReload] = useState(false);
    const [budget, setBudget] = useState(null);
    const [budgetItems, setBudgetItems] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        getBudget(budgetId).then(setBudget).catch(console.warn);
        getBudgetItems(budgetId).then(setBudgetItems).catch(console.warn);
        setLoading(false);
    }, [budgetId, reload]);

    function handleReload() {
        setReload(reload => !reload);
    }

    if (error) {
        return <Error error={error} />;
    }

    if (loading) {
        return <span>Loading</span>;
    }

    return (
        <Skeleton loading={loading}>
            <div>
                <div>
                    <BudgetTitle {...{ budgetId, name, totalLimit, handleReload }} />
                    <Divider style={{ marginTop: 8, marginBottom: 8 }} />
                    {budgetItems?.map(item => (
                        <>
                            <BudgetItem
                                tag={item.l1}
                                tagColor={'red'}
                                amount={item.amount}
                                used={0}
                            />
                        </>
                    ))}
                </div>
            </div>
        </Skeleton>
    );
}

function BudgetTitle({ budgetId, name, totalLimit, handleReload }) {
    return (
        <div
            style={{
                display: 'flex',
                justifyItems: 'end',
                justifyContent: 'space-between',
                width: '100%',
            }}
        >
            <div>
                <h1>
                    {name} - [{budgetId}]{' '}
                </h1>
                <span>£{totalLimit}</span>
            </div>
            <Button onClick={handleReload}>
                <ReloadOutlined />
            </Button>
        </div>
    );
}
