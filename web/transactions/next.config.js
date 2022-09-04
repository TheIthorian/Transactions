/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    swcMinify: true,
};

const path = require('path');
module.exports = {
    nextConfig,
    webpack: config => {
        config.resolve.modules.push(path.resolve('./'));

        return config;
    },
};
