#!/usr/bin/env bash
set -e

ROOT="$(pwd)"
BACKUP="$ROOT/backup_project_$(date +%s)"
echo "Backing up project to $BACKUP"
mkdir -p "$BACKUP"
cp -a app "$BACKUP/" || true
cp -a package.json "$BACKUP/" || true
cp -a package-lock.json "$BACKUP/" || true
cp -a tailwind.config.* "$BACKUP/" 2>/dev/null || true
cp -a postcss.config.* "$BACKUP/" 2>/dev/null || true

echo "Writing canonical files..."

# Force Flask to use app/templates
cat > app/__init__.py <<'PY'
from flask import Flask
from .extensions import db, migrate, login_manager
from .config import Config

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.blueprints.core import core_bp
    from app.blueprints.dashboard import dashboard_bp
    try:
        from app.blueprints.api.v1 import api_v1_bp
        app.register_blueprint(api_v1_bp, url_prefix="/api/v1")
    except Exception:
        pass

    app.register_blueprint(core_bp)
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    return app
PY

# Create canonical base.html
mkdir -p app/templates
cat > app/templates/base.html <<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{% block title %}TaskFlow{% endblock %}</title>
  <link href="{{ url_for('static', filename='css/app.css') }}?v={{ config.get('SECRET_KEY','v1') }}" rel="stylesheet" />
  <style>html,body,#app-root { height: 100%; }</style>
</head>
<body class="bg-slate-50 text-slate-800" id="app-root">
  <div class="min-h-full flex">
    <aside class="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0 bg-white border-r">
      <div class="flex-1 flex flex-col min-h-0">
        <div class="px-6 py-4">
          <a href="{{ url_for('core.home') }}" class="inline-flex items-center gap-3">
            <div class="h-10 w-10 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold">TF</div>
            <span class="text-xl font-semibold text-slate-900">TaskFlow</span>
          </a>
        </div>
        <nav class="px-4 py-6 space-y-1">
          <a href="{{ url_for('dashboard.home') }}" class="block px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-100">Dashboard</a>
          <a href="#" class="block px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-100">Tasks</a>
          <a href="#" class="block px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-100">Projects</a>
          <a href="#" class="block px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-100">Analytics</a>
          <a href="#" class="block px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-100">Settings</a>
        </nav>
        <div class="mt-auto px-4 py-4">
          <a href="#" class="block text-sm text-slate-600 hover:text-slate-800">Your Account</a>
        </div>
      </div>
    </aside>

    <div class="flex-1 md:pl-64">
      <header class="sticky top-0 z-10 bg-white border-b">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="h-16 flex items-center justify-between">
            <div class="flex items-center gap-4">
              <button id="mobile-menu-btn" class="md:hidden inline-flex items-center justify-center p-2 rounded-md text-slate-500 hover:bg-slate-100">
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
              </button>
              <div class="text-lg font-semibold text-slate-900">{% block header_title %}Dashboard{% endblock %}</div>
            </div>
            <div class="flex items-center gap-4">
              <div class="hidden sm:flex items-center gap-4">
                <input type="search" placeholder="Search..." class="px-3 py-2 rounded-md border bg-slate-50 text-sm" />
              </div>
              <div class="flex items-center gap-3">
                <button class="px-3 py-2 text-sm rounded-md hover:bg-slate-100">Docs</button>
                <a href="#" class="inline-flex items-center px-3 py-2 bg-indigo-600 text-white text-sm rounded-md">Get Started</a>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main>
        <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div class="mb-6">
            <h1 class="text-3xl font-bold text-slate-900">{% block page_title %}{% endblock %}</h1>
            <p class="mt-2 text-sm text-slate-600">{% block page_subtitle %}{% endblock %}</p>
          </div>
          {% block content %}{% endblock %}
        </div>
      </main>
    </div>
  </div>

  <div id="mobile-drawer" class="fixed inset-0 z-40 md:hidden hidden">
    <div class="absolute inset-0 bg-black/30" id="mobile-drawer-backdrop"></div>
    <div class="absolute left-0 top-0 bottom-0 w-64 bg-white p-4">
      <div class="mb-4">
        <a href="{{ url_for('core.home') }}" class="inline-flex items-center gap-3">
          <div class="h-9 w-9 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold">TF</div>
          <span class="text-lg font-semibold text-slate-900">TaskFlow</span>
        </a>
      </div>
      <nav class="space-y-1">
        <a class="block px-3 py-2 rounded text-slate-700 hover:bg-slate-100" href="{{ url_for('dashboard.home') }}">Dashboard</a>
        <a class="block px-3 py-2 rounded text-slate-700 hover:bg-slate-100" href="#">Tasks</a>
      </nav>
    </div>
  </div>

  <script>
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const drawer = document.getElementById('mobile-drawer');
    const backdrop = document.getElementById('mobile-drawer-backdrop');
    function openDrawer() { drawer.classList.remove('hidden'); }
    function closeDrawer() { drawer.classList.add('hidden'); }
    if (mobileBtn) mobileBtn.addEventListener('click', openDrawer);
    if (backdrop) backdrop.addEventListener('click', closeDrawer);
  </script>
</body>
</html>
HTML

# canonical home
mkdir -p app/templates/dashboard
cat > app/templates/dashboard/home.html <<'HTML'
{% extends "base.html" %}
{% block title %}Dashboard — TaskFlow{% endblock %}
{% block header_title %}Dashboard{% endblock %}
{% block page_title %}Welcome to TaskFlow{% endblock %}
{% block page_subtitle %}Your productivity dashboard{% endblock %}

{% block content %}
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
  <div class="bg-white p-6 rounded-lg border">
    <h3 class="text-sm text-slate-600">Tasks Due</h3>
    <div class="mt-4 text-3xl font-bold">{{ tasks_due }}</div>
    <p class="text-sm text-slate-500 mt-1">In the next few days</p>
  </div>
  <div class="bg-white p-6 rounded-lg border">
    <h3 class="text-sm text-slate-600">Completed</h3>
    <div class="mt-4 text-3xl font-bold">{{ completed }}</div>
    <p class="text-sm text-slate-500 mt-1">This month</p>
  </div>
  <div class="bg-white p-6 rounded-lg border">
    <h3 class="text-sm text-slate-600">Projects</h3>
    <div class="mt-4 text-xl font-semibold">{{ projects|length }}</div>
    <p class="text-sm text-slate-500 mt-1">Active projects</p>
  </div>
</div>

<div class="bg-white mt-8 p-6 rounded-lg border">
  <h3 class="text-lg font-semibold text-slate-800 mb-4">Recent Tasks</h3>
  {% if recent_tasks %}
  <ul class="divide-y">
    {% for task in recent_tasks %}
    <li class="py-3 flex justify-between">
      <span class="font-medium text-slate-700">{{ task.title }}</span>
      <span class="text-sm text-slate-500">{{ task.created_at.strftime('%d %b') }}</span>
    </li>
    {% endfor %}
  </ul>
  {% else %}
  <p class="text-slate-500 text-sm">No recent tasks.</p>
  {% endif %}
</div>
{% endblock %}
HTML

# tailwind input
mkdir -p app/static/css
cat > app/static/css/tailwind.css <<'CSS'
@tailwind base;
@tailwind components;
@tailwind utilities;
CSS

# tailwind config (cjs)
cat > tailwind.config.cjs <<'JS'
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/blueprints/**/templates/**/*.html",
    "./app/static/js/**/*.js",
    "./app/**/*.html"
  ],
  theme: { extend: {} },
  plugins: [],
}
JS

# package.json safe
cat > package.json <<'JSON'
{
  "name": "taskflow",
  "version": "1.0.0",
  "description": "TaskFlow Web App",
  "scripts": {
    "dev": "npx tailwindcss -i ./app/static/css/tailwind.css -o ./app/static/css/app.css --watch",
    "build": "npx tailwindcss -i ./app/static/css/tailwind.css -o ./app/static/css/app.css"
  },
  "devDependencies": {
    "tailwindcss": "^3.4.0",
    "postcss": "^8.0.0",
    "autoprefixer": "^10.0.0"
  }
}
JSON

echo "Attempting npm install (optional)..."
if command -v npm >/dev/null 2>&1; then
  npm install --no-audit --no-fund || true
else
  echo "npm not found; please run 'npm install' later."
fi

echo "Building tailwind once..."
npx tailwindcss -i ./app/static/css/tailwind.css -o ./app/static/css/app.css || true

echo "Done. Created backup at $BACKUP"
ls -lh app/static/css/app.css || true
