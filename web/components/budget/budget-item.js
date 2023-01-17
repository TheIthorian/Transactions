import { DeleteOutlined } from '@ant-design/icons';
import { Button, Input, Progress } from 'antd';
import { updateBudgetItem } from './data';

export function BudgetItem({ id, budgetId, tag, tagColor, amount, spent, onDelete }) {
    let t;
    const spentAmount = spent ?? 0;
    const spentPercent = Math.max(spentAmount, 0) / amount;

    function handleChangeAmount(event) {
        clearTimeout(t);
        if (event.target.value) {
            t = setTimeout(() => {
                updateBudgetItem(id, budgetId, event.target.value);
            }, 300);
        }
    }

    function handleDelete() {
        onDelete(id);
    }

    return (
        <div style={{ width: '100%', padding: 5 }}>
            <div>
                <span>{tag}</span>
                <br />
                <div style={{ display: 'flex', alignItems: 'baseline', width: '100%' }}>
                    <span>
                        {spentAmount} /{' '}
                        <Input
                            defaultValue={amount}
                            style={{ padding: 2, width: 'fit-content' }}
                            onChange={handleChangeAmount}
                            type='number'
                        />
                    </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'baseline', width: '100%' }}>
                    <Progress
                        percent={100 * spentPercent}
                        strokeColor={tagColor}
                        showInfo={false}
                    />
                    <Button size='small' style={{ marginLeft: 15 }} onClick={handleDelete}>
                        <DeleteOutlined size='small' />
                    </Button>
                </div>
            </div>
        </div>
    );
}
