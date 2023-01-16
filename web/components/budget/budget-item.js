export function BudgetItem({ tag, tagColor, amount, used }) {
    return (
        <div style={{ backgroundColor: tagColor, width: '100%', padding: 5 }}>
            <div>
                <span>
                    {tag} - {used} / {amount}
                </span>
            </div>
            {/* {JSON.stringify({ tag, tagColor, amount, used })} */}
        </div>
    );
}
