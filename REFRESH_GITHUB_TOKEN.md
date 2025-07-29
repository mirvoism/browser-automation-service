# 🔑 Manual GitHub Token Refresh (2 minutes)

Since GitHub CLI is having prompt issues, let's refresh your token manually:

## Step 1: Create New Personal Access Token

1. **Go to**: https://github.com/settings/tokens
2. **Click**: "Generate new token" → "Generate new token (classic)"
3. **Note**: "Terminal/CLI Access" 
4. **Expiration**: 90 days (or custom)
5. **Scopes** - Check these boxes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `write:packages` (Upload packages)
   - ✅ `delete:packages` (Delete packages)

6. **Click**: "Generate token"
7. **Copy** the token (starts with `ghp_...`)

## Step 2: Set the New Token

```bash
# Set the new token (replace YOUR_NEW_TOKEN with the actual token)
export GITHUB_TOKEN="YOUR_NEW_TOKEN"

# Test it works
gh auth status
```

## Step 3: Create Repository 

Once the token works:

```bash
# Create the repository
gh repo create ai-browser-automation --public --description "Visual AI browser automation with Google Gemini and Mac Studio Ollama support"

# Add remote and push
git remote add origin https://github.com/$(gh api user --jq .login)/ai-browser-automation.git
git push -u origin main
```

## Alternative: Quick Manual Approach

If you prefer not to refresh the token right now:

1. **Go to**: https://github.com/new
2. **Create** repository manually 
3. **Push** with:
   ```bash
   git remote add origin https://github.com/YOURUSERNAME/ai-browser-automation.git
   git push -u origin main
   ```

---

## 💡 Why This Happens

The GitHub CLI sometimes has issues with terminal prompts. Manual token creation is often more reliable and gives you direct control over permissions.

**Choose whichever method is easier for you!** 🚀 