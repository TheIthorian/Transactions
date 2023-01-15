import Link from 'next/link';
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
                    { key: 'Home', label: <Link href='/'>Home</Link> },
                    { key: 'Budget', label: <Link href='/budget'>Budget</Link> },
                    { key: 'Settings', label: <Link href='/'>Settings</Link> },
                ]}
            />
        </>
    );
}

export default Nav;
