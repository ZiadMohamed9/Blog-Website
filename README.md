# Blog Website

## Overview

This Flask-based blog website supports role-based access control with three distinct roles: Admin, Author, and Reader. Each role has specific privileges and access levels, providing a comprehensive platform for managing and interacting with blog posts.

## Features

### General Features
- **User Authentication**: Users can register, log in, and log out.
- **Role-Based Access Control**: Different privileges for Admin, Author, and Reader roles.

### Admin Features
- **Dashboard**: Admins have access to a dashboard to manage all blog posts and users.
- **User Management**: Promote users to Author or Admin roles, or delete users.
- **Blog Management**: Full control over all blog posts including creating, viewing, editing, and deleting.

### Author Features
- **Dashboard**: Authors have a personal dashboard to manage their own posts.
- **Post Management**: Create, view, edit, and delete only their own blog posts.

### Reader Features
- **View Posts**: Readers can view all published blog posts.
- **Like/Dislike**: Readers can like or dislike blog posts.
- **Comments**: Readers can add comments to blog posts and view existing comments.
