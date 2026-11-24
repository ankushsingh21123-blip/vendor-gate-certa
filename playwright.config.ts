import{defineConfig}from'@playwright/test';
export default defineConfig({testDir:'.',testMatch:'browser.spec.ts',workers:1,use:{baseURL:'http://127.0.0.1:4178',headless:true},webServer:{command:(process.env.VENDOR_TEST_SERVER||'python api/index.py'),url:'http://127.0.0.1:4178/api/health',reuseExistingServer:true}})
