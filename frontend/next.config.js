/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "ci.encar.com",
      },
    ],
  },
};

module.exports = nextConfig;
