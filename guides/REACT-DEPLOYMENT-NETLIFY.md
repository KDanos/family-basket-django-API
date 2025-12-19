![ga_cog_large_red_rgb](https://cloud.githubusercontent.com/assets/40461/8183776/469f976e-1432-11e5-8199-6ac91363302b.png)

# Netlify Deployment React
We'll be deploying our Express/Django RESTful APIs separately. React apps can always be deployed by Netlify, so the below steps can be used irregardless of the server-side you choose to connect it to.

## 1. Netlify configuration

### Add a netlify.toml file
In the root of your React App directory, add a file named `netlify.toml` and copy the below contents into it:

```
[build]
  command = "npm run build"
  functions = "netlify/functions"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## 2. Netlify Deployment
As with the API deployment, log into [Netlify](/https://app.netlify.com/) and click "Add new project" followed by "Import an existing project".

Select "Github" and then find your React App repo.

On the configuration page, ensure the following values are set:
- "Build command": `npm run build`
- "Publish directory": `dist`
- "Environment variables": Import all your variables but ensure the API URL variable (whatever you've called it) is set to your deployed URL, e.g: `VITE_API_URL=https://my-api.netlify.app/api`

You can ignore the serverless functions field, this won't use them and it can stay prefilled as it is.

## Finished
This is the whole process. Any further pushes to Github from this repo will redeploy your site, as with the API deployment.

## Errors
If you get any errors during deployment, you will see them in the `🚀 Deploys` tab. Click on the most recent failed deploy, and you should get some more information about what happened. Try and solve them yourself, but ask us if you can't work out how to fix them problem.