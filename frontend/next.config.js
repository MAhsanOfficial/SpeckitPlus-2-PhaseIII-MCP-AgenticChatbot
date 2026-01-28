/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // Enable experimental features for better Docker compatibility
  experimental: {
    // Optimize for production builds
    optimizePackageImports: ['lucide-react'],
  },
}

module.exports = nextConfig
