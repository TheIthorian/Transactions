import { ReloadOutlined } from '@ant-design/icons';
import { Button, Divider, Skeleton } from 'antd';
import { useEffect, useState } from 'react';
import { BudgetItem } from './budget-item';
import { addBudgetItem, deleteBudgetItem, getBudgetItems } from './data';
import { TagSelection } from './tagSelection';

export default function Budget({ budgetId, name, totalLimit }) {
    const [loading, setLoading] = useState(true);
    const [reload, setReload] = useState(false);
    const [budgetItems, setBudgetItems] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        getBudgetItems(budgetId).then(setBudgetItems).catch(console.warn);
        setLoading(false);
    }, [budgetId, reload]);

    function handleReload() {
        setReload(reload => !reload);
    }

    function handleAddBudgetItem(value) {
        // This produces NaN and does not provide the new id
        const newItem = { l1: value, amount: 0 };
        setBudgetItems(originalItems => [...originalItems, newItem]);
        addBudgetItem(budgetId, newItem);
    }

    function handleDelete(id) {
        deleteBudgetItem(id, budgetId);
        setBudgetItems(originalItems => originalItems.filter(item => item.id !== id));
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
                    {budgetItems.map(item => (
                        <div key={item.l1} style={{ marginTop: 10 }}>
                            <BudgetItem
                                id={item.id}
                                budgetId={budgetId}
                                tag={item.l1}
                                tagColor={item.tagColor}
                                amount={item.amount}
                                spent={-item.spent}
                                onDelete={handleDelete}
                            />
                        </div>
                    ))}
                    <TagSelection budgetId={budgetId} onAdd={handleAddBudgetItem} />
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
