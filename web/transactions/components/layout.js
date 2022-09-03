import { Layout } from 'antd';

import Nav from '../components/header';

const { Header, Content, Footer } = Layout;

export default function _Layout({ children }) {
    return (
        <div>
            <Layout style={{ minHeight: '100vh' }}>
                <Header
                    style={{
                        position: 'fixed',
                        zIndex: 1,
                        width: '100%',
                    }}
                >
                    <Nav />
                </Header>
                <Content
                    className='site-layout'
                    style={{
                        padding: '0 50px',
                        marginTop: 64,
                    }}
                >
                    {children}
                </Content>
                <Footer
                    style={{
                        textAlign: 'center',
                    }}
                >
                    Transactions
                </Footer>
            </Layout>
        </div>
    );
}
