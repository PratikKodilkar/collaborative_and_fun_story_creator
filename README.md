# Collaborative and Fun Story Creator

A web application for collaborative storytelling where users can create stories and contribute to existing ones, fostering creativity and community engagement.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Future Enhancements](#future-enhancements)

## Project Overview

The Collaborative and Fun Story Creator allows multiple users to create and build upon each other's stories. Users can register, log in, start new stories, or contribute to existing ones with text and images, creating a rich storytelling experience. 

## Features

- **User Registration & Authentication**: Register, log in, and access features with secure JWT-based authentication.
- **Story Creation**: Users can create and publish new stories with a title and optional image.
- **Collaborative Contributions**: Up to four users can contribute to a story, enhancing the narrative with their own additions.
- **Image Upload with Validation**: Users can upload images with their stories, validated for size and filename requirements.
- **Comprehensive Story Retrieval**: Retrieve complete stories along with all contributions.
- **Logs & Middleware**: Middleware logs capture the details of creators and contributors for each story.

## Technologies Used

- **Backend**: Django, Django Rest Framework (DRF)
- **Database**: PostgreSQL (production), SQLite (development)
- **Authentication**: JSON Web Tokens (JWT) for secure access
- **API Documentation**: Postman or Swagger (optional)
- **Image Storage**: Django’s file upload system with custom validation

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/PratikKodilkar/collaborative_and_fun_story_creator.git
   cd collaborative_and_fun_story_creator