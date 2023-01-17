import { Card } from 'antd';
import { useEffect, useState } from 'react';

import { Error } from 'components/error';
import Budget from 'components/budget';

import { getBudgets } from './data';

export default function Budgets() {
    const [budgets, setBudgets] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        getBudgets().then(setBudgets).catch(setError);
    }, []);

    if (error) {
        return <Error error={error} />;
    }

    return (
        <Card style={{ marginTop: 10 }} bodyStyle={{ padding: 15 }}>
            {budgets.map(budget => (
                <Budget
                    budgetId={budget.id}
                    name={budget.name}
                    totalLimit={budget.totalLimit}
                    key={budget.id}
                />
            ))}
        </Card>
    );
}
