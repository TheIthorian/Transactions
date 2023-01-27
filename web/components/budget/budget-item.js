import { useState } from 'react';
import { DeleteOutlined } from '@ant-design/icons';
import { Button, Input, Progress } from 'antd';

export function BudgetItem({ id, tag, tagColor, amount, spent, onDelete, onUpdate }) {
    let t;
    const spentAmount = spent ?? 0;
    const spentPercent = Math.max(spentAmount, 0) / amount;

    function handleChangeAmount(event) {
        clearTimeout(t);
        const newAmount = event.target.value;
        if (newAmount) {
            t = setTimeout(() => {
                onUpdate(id, newAmount);
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
