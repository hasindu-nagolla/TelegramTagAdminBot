# 🌐 Custom Domain Setup Guide

## Current Configuration

- **Custom Domain**: `atziobot.hasindunagolla.live`
- **GitHub Pages**: Enabled
- **CNAME File**: Created in `public/CNAME`

## 📝 Step-by-Step Setup

### 1. Configure DNS in Cloudflare

Based on your screenshot, you need to add a **CNAME record** for the subdomain:

1. Go to your Cloudflare dashboard for `hasindunagolla.live`
2. Navigate to **DNS** → **Records**
3. Click **Add record**
4. Configure:
   - **Type**: `CNAME`
   - **Name**: `atziobot` (subdomain)
   - **Target**: `hasindu-nagolla.github.io`
   - **Proxy status**: Proxied (orange cloud) ✅
   - **TTL**: Auto

**Important**: The target should be `hasindu-nagolla.github.io` (your GitHub username + github.io)

### 2. Push Code to GitHub

```bash
git add .
git commit -m "Add custom domain support"
git push origin main
```

This will trigger the GitHub Actions workflow.

### 3. Configure GitHub Pages

1. Go to your repository: `https://github.com/hasindu-nagolla/telegram-admin-mention-bot`
2. Settings → Pages
3. Under **Build and deployment**:
   - Source: **GitHub Actions**
4. Under **Custom domain**:
   - Enter: `atziobot.hasindunagolla.live`
   - Click **Save**
   - Wait for DNS check (may take a few minutes)
   - ✅ Enable **Enforce HTTPS** (after DNS check passes)

### 4. Verify Deployment

Wait 2-5 minutes after pushing, then:

1. Check GitHub Actions tab for deployment status
2. Visit: `https://atziobot.hasindunagolla.live`
3. Your site should be live! 🎉

## 🔍 DNS Configuration in Cloudflare

### What You Need (CNAME Record)

| Type | Name | Target | Proxy | TTL |
|------|------|--------|-------|-----|
| CNAME | atziobot | hasindu-nagolla.github.io | ✅ Proxied | Auto |

### Current Records (From Your Screenshot)

I can see you already have several records. Make sure to **add** the CNAME record above.

## 🛠️ Troubleshooting

### Issue: DNS_PROBE_POSSIBLE or "Site can't be reached"

**Solutions**:
1. **Wait for DNS propagation** (can take 5-60 minutes)
2. **Check CNAME record** in Cloudflare:
   - Name: `atziobot`
   - Target: `hasindu-nagolla.github.io` (NOT the full domain)
3. **Verify GitHub Pages custom domain** is set correctly
4. **Clear browser cache** or try incognito mode

### Issue: GitHub Pages says "DNS check failed"

**Solutions**:
1. Make sure CNAME record points to `hasindu-nagolla.github.io`
2. Wait a few minutes for DNS to propagate
3. Try removing and re-adding the custom domain in GitHub settings

### Issue: "404 - There isn't a GitHub Pages site here"

**Solutions**:
1. Make sure GitHub Actions deployment completed successfully
2. Check that `CNAME` file exists in the `dist` folder after build
3. Verify GitHub Pages is enabled with GitHub Actions as source

### Issue: HTTPS not working

**Solutions**:
1. Wait 24 hours for GitHub to provision SSL certificate
2. Make sure Cloudflare proxy is enabled (orange cloud)
3. In Cloudflare SSL/TLS settings, set to "Full" or "Full (strict)"

## 🔐 Cloudflare SSL/TLS Settings

1. Go to Cloudflare → SSL/TLS
2. Set encryption mode to: **Full** or **Full (strict)**
3. This ensures HTTPS works correctly

## ✅ Checklist

- [ ] CNAME record added in Cloudflare DNS
- [ ] Code pushed to GitHub (with public/CNAME file)
- [ ] GitHub Actions deployment successful
- [ ] Custom domain configured in GitHub Pages settings
- [ ] DNS check passed on GitHub
- [ ] HTTPS enabled on GitHub Pages
- [ ] Site accessible at https://atziobot.hasindunagolla.live

## 🚀 Quick Command Reference

```bash
# Build locally to test
npm run build

# Check if CNAME file is in dist folder
ls dist/CNAME  # PowerShell: dir dist/CNAME

# Push to deploy
git add .
git commit -m "Deploy to custom domain"
git push origin main
```

## 📊 Expected Timeline

- **Push to GitHub**: Immediate
- **GitHub Actions build**: 2-3 minutes
- **DNS propagation**: 5-60 minutes
- **SSL certificate**: Up to 24 hours (usually within 1 hour)

## 🔗 Useful Links

- **Your site**: https://atziobot.hasindunagolla.live
- **Cloudflare DNS**: https://dash.cloudflare.com (your domain's DNS section)
- **GitHub Pages settings**: https://github.com/hasindu-nagolla/telegram-admin-mention-bot/settings/pages
- **GitHub Actions**: https://github.com/hasindu-nagolla/telegram-admin-mention-bot/actions

## 📞 Still Not Working?

If after 1 hour your site isn't working:

1. **Check DNS propagation**: https://www.whatsmydns.net/#CNAME/atziobot.hasindunagolla.live
2. **Check GitHub Actions logs** for errors
3. **Verify CNAME record** in Cloudflare matches exactly: `hasindu-nagolla.github.io`
4. **Try accessing**: https://hasindu-nagolla.github.io/telegram-admin-mention-bot/ (backup URL)

---

**Next Step**: Add the CNAME record in Cloudflare DNS as shown above! 🎯
