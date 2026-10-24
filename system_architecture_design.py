             FLEETPULSE SYSTEM ARCHITECTURE

                    ┌───────────────────┐
                    │       USER        │
                    │ Admin / Fleet Mgr │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   PRESENTATION    │
                    │      LAYER        │
                    │                   │
                    │ HTML              │
                    │ CSS               │
                    │ JavaScript        │
                    │ Chart.js          │
                    └─────────┬─────────┘
                              │
                        HTTP / JSON
                              │
                              ▼
                    ┌───────────────────┐
                    │ APPLICATION LAYER │
                    │                   │
                    │ Python Flask API  │
                    │                   │
                    │ Login Validation  │
                    │ Vehicle Management│
                    │ Maintenance       │
                    │ Service History   │
                    │ Analytics          │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │    DATA LAYER     │
                    │                   │
                    │  SQLite Database  │
                    │                   │
                    │  Vehicles Table   │
                    │  Maintenance Table│
                    └───────────────────┘
