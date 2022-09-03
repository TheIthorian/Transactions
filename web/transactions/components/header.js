import { Menu } from 'antd';
import 'antd/dist/antd.css';

function Nav() {
    return (
        <>
            <div className='logo' />
            <Menu
                theme='dark'
                mode='horizontal'
                defaultSelectedKeys={['1']}
                items={[
                    { key: 'Home', label: 'Home' },
                    { key: 'Transactions', label: 'Transactions' },
                    { key: 'Settings', label: 'Settings' },
                ]}
            />
        </>
    );
}

export default Nav;
