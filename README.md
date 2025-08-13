# Atlas - The Joy of Painting API

A complete ETL pipeline and REST API for filtering Bob Ross "The Joy of Painting" episodes by month, subject matter, and color palette.

## Project Overview

This project extracts data from multiple CSV sources, transforms it for consistency, and loads it into MongoDB. The API allows filtering of 403 episodes based on:
- Month of original broadcast
- Subject matter (mountains, trees, cabins, etc.)
- Color palette (specific paint colors used)

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup MongoDB**
   - Install MongoDB locally or use MongoDB Atlas
   - Update connection string in `config.py`

3. **Run ETL Process**
   ```bash
   python run_etl.py
   ```

4. **Start API Server**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Get All Episodes
```
GET /episodes
```

### Get Episode by ID
```
GET /episodes/<id>
```

### Filter Episodes
```
GET /episodes/filter?month=january&subjects=mountain,tree&colors=prussian_blue&match=all
POST /episodes/filter
```

### Get Colors and Subjects
```
GET /colors
GET /subjects
```

## Example API Calls

### Filter by Month
```bash
curl "http://localhost:5000/episodes/filter?month=january"
```

### Filter by Multiple Subjects (ANY match)
```bash
curl "http://localhost:5000/episodes/filter?subjects=mountain,tree&match=any"
```

### Filter by Colors (ALL match)
```bash
curl "http://localhost:5000/episodes/filter?colors=Prussian Blue,Titanium White&match=all"
```

### Combined Filters
```bash
curl "http://localhost:5000/episodes/filter?month=january&subjects=mountain&colors=prussian_blue&match=all"
```

## Data Sources

- **Episode Dates**: Episode titles with air dates
- **Colors Used**: Paint colors and hex codes for each episode  
- **Subject Matter**: Binary indicators for subjects featured in each episode

## Filter Logic

- **match=any**: Returns episodes that match ANY of the specified filters
- **match=all**: Returns episodes that match ALL of the specified filters

## Testing

Use Postman or curl to test the API endpoints. The API returns JSON responses with episode data including:
- Episode details (title, season, episode number, air date)
- Associated colors and subjects
- YouTube links and painting images


