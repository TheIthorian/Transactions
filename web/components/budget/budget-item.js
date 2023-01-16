import { Input, Progress } from 'antd';
import { updateBudgetItem } from './data';

export function BudgetItem({ id, budgetId, tag, tagColor, amount, used }) {
    let t;

    function handleChangeAmount(event) {
        clearTimeout(t);
        t = setTimeout(() => {
            updateBudgetItem(id, budgetId, event.target.value);
        }, 300);
    }

    return (
        <div style={{ width: '100%', padding: 5 }}>
            <div>
                <span>{tag}</span>
                <br />
                <div style={{ display: 'flex', alignItems: 'baseline', width: '100%' }}>
                    <span>
                        {used} /{' '}
                        <Input
                            defaultValue={amount}
                            style={{ padding: 2, width: 'fit-content' }}
                            onChange={handleChangeAmount}
                        />
                    </span>
                </div>
                <Progress percent={100 * (10 / amount)} strokeColor={tagColor} showInfo={false} />
            </div>
        </div>
    );
}
