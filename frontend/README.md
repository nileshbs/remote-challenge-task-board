# Task Manager Frontend - Refactored

A modern, well-structured Vue.js 3 frontend application for the Task Manager project, following SOLID principles and Vue best practices.

## 🏗️ Architecture Overview

The application follows a clean, modular architecture with clear separation of concerns:

```
src/
├── config/                 # Configuration and constants
│   └── index.js           # Centralized configuration
├── composables/           # Reusable Vue composables
│   ├── useAuth.js         # Authentication logic
│   ├── useTasks.js        # Task management logic
│   ├── useDragDrop.js     # Drag and drop functionality
│   └── useNotifications.js # Notification system
├── components/            # Reusable Vue components
│   ├── TaskBoardHeader.vue # Header component
│   ├── TaskColumn.vue     # Task column component
│   ├── TaskCard.vue       # Individual task card
│   ├── DeleteZone.vue     # Delete drop zone
│   ├── LoadingOverlay.vue # Loading indicator
│   ├── NotificationContainer.vue # Notification display
│   ├── AddTaskDialog.vue  # Add task modal
│   └── EditTaskDialog.vue # Edit task modal
├── services/              # API services
│   └── api.js            # Comprehensive API layer
├── utils/                 # Utility functions
│   └── index.js          # Common utilities
├── views/                 # Page components
│   ├── Login.vue         # Login page
│   └── TaskBoard.vue     # Main task board
├── router/               # Vue Router configuration
│   └── index.js         # Route definitions and guards
├── App.vue              # Root component
└── main.js              # Application entry point
```

## 🎯 SOLID Principles Implementation

### Single Responsibility Principle (SRP)
- Each module has one clear purpose
- Composables handle specific functionality
- Components are focused and single-purpose

### Open/Closed Principle (OCP)
- Composables can be extended without modification
- Components accept props for customization
- Services use interfaces for extensibility

### Liskov Substitution Principle (LSP)
- All composables follow consistent interfaces
- Components can be substituted with compatible props

### Interface Segregation Principle (ISP)
- Composables provide focused, specific functionality
- No client depends on unused methods

### Dependency Inversion Principle (DIP)
- Components depend on composables (abstractions)
- High-level modules don't depend on low-level modules

## 🚀 Key Features

### ✅ Modern Architecture
- **Vue 3 Composition API**: Modern reactive programming
- **Composables**: Reusable logic with clear interfaces
- **Configuration Management**: Centralized settings
- **Error Handling**: Comprehensive error management
- **Type Safety**: Input validation and data integrity

### ✅ User Experience
- **Authentication**: Secure login with token management
- **Task Board**: Three-column Kanban board (To Do, In Progress, Completed)
- **Drag & Drop**: Native HTML5 drag and drop with visual feedback
- **Notifications**: Toast notifications for user feedback
- **Loading States**: Visual feedback during operations
- **Responsive Design**: Works on desktop and mobile devices

### ✅ Developer Experience
- **Hot Reload**: Fast development iteration
- **Error Logging**: Comprehensive error logging
- **Code Organization**: Clear separation of concerns
- **Reusable Logic**: Composables for common functionality
- **Testing Ready**: Structure supports easy testing

## 🛠️ Setup Instructions

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## ⚙️ Configuration

The application uses centralized configuration in `src/config/index.js`:

```javascript
export const CONFIG = {
  API: {
    BASE_URL: 'http://10.0.0.8:8000',
    TIMEOUT: 10000,
    RETRY_ATTEMPTS: 3
  },
  APP: {
    NAME: 'Task Manager',
    VERSION: '1.0.0'
  },
  TASK: {
    STATUSES: {
      TODO: 'To Do',
      IN_PROGRESS: 'In Progress',
      COMPLETED: 'Completed'
    }
  }
}
```

## 🔧 Composables

### useAuth
Manages authentication state and operations:
```javascript
const { userData, isLoggedIn, login, logout } = useAuth()
```

### useTasks
Handles task management operations:
```javascript
const { allTasks, loading, createTask, updateTask, deleteTask } = useTasks()
```

### useDragDrop
Provides drag and drop functionality:
```javascript
const { handleDragStart, handleDrop, dragOverColumn } = useDragDrop()
```

### useNotifications
Manages notification system:
```javascript
const { showSuccess, showError, taskNotifications } = useNotifications()
```

## 🎨 Components

### TaskBoard
Main application component that orchestrates all functionality:
- Uses composables for state management
- Handles drag and drop operations
- Manages dialog states

### TaskCard
Individual task display component:
- Props validation with custom validators
- Drag and drop support
- Action buttons for edit/delete

### TaskColumn
Column component for task organization:
- Drop zone functionality
- Task count display
- Empty state handling

## 🔒 Security Features

### Authentication
- JWT token-based authentication
- Automatic token refresh and logout on expiration
- Route guards to protect authenticated pages
- Secure token storage with expiry

### Input Validation
- Comprehensive form validation
- Data sanitization
- Error message sanitization

### Error Handling
- No sensitive information in error messages
- Safe error logging practices
- User-friendly error messages

## 📱 Responsive Design

- **Mobile-first approach**: Optimized for mobile devices
- **Flexible layouts**: CSS Grid and Flexbox
- **Touch-friendly**: Large touch targets
- **Adaptive UI**: Components adapt to screen size

## 🧪 Testing

The application is structured for easy testing:

### Component Testing
```javascript
// Example component test
import { mount } from '@vue/test-utils'
import TaskCard from '@/components/TaskCard.vue'

test('renders task title', () => {
  const wrapper = mount(TaskCard, {
    props: { task: { title: 'Test Task' } }
  })
  expect(wrapper.text()).toContain('Test Task')
})
```

### Composable Testing
```javascript
// Example composable test
import { useTasks } from '@/composables/useTasks'

test('loads tasks', async () => {
  const { loadTasks, allTasks } = useTasks()
  await loadTasks()
  expect(allTasks.value).toBeDefined()
})
```

## 🚀 Performance

### Optimizations
- **Tree Shaking**: Unused code elimination
- **Code Splitting**: Lazy loading of routes
- **Efficient Rendering**: Vue 3 reactivity optimizations
- **Memory Management**: Proper cleanup and disposal

### Bundle Analysis
```bash
npm run build -- --analyze
```

## 🔧 Development

### Code Quality
- **ESLint**: Code linting and style enforcement
- **Prettier**: Code formatting
- **Type Safety**: Input validation and prop validation
- **Documentation**: Comprehensive JSDoc comments

### Debugging
- **Vue DevTools**: Enhanced debugging with Vue DevTools
- **Error Logging**: Comprehensive error logging
- **Performance Monitoring**: Built-in performance tracking

## 🌐 Browser Support

- **Chrome** (recommended)
- **Firefox**
- **Safari**
- **Edge**

## 📊 Demo Credentials

Use these credentials to test the application:

- **Username**: johndoe
- **Password**: password123

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the backend CORS configuration includes your frontend URL
2. **API Connection**: Verify the backend server is running on the correct port
3. **Authentication**: Clear localStorage if experiencing login issues
4. **Build Errors**: Check Node.js version compatibility

### Development Tips

- Use browser dev tools to inspect network requests
- Check the console for any JavaScript errors
- Verify API responses in the Network tab
- Use Vue DevTools for component debugging

## 📈 Future Enhancements

### Planned Features
- **TypeScript Support**: Full TypeScript implementation
- **PWA Support**: Progressive Web App capabilities
- **Offline Support**: Offline task management
- **Real-time Updates**: WebSocket integration
- **Advanced Filtering**: Task filtering and search
- **Task Categories**: Category-based organization

### Performance Improvements
- **Virtual Scrolling**: For large task lists
- **Image Optimization**: Lazy loading and optimization
- **Caching Strategy**: Advanced caching implementation
- **Bundle Optimization**: Further bundle size reduction

## 🤝 Contributing

1. Follow Vue.js best practices
2. Use composables for reusable logic
3. Add comprehensive tests for new features
4. Update documentation
5. Follow SOLID principles
6. Ensure responsive design

## 📄 License

This project is part of a coding challenge and is for educational purposes.

---

**Built with ❤️ using Vue.js 3, Composition API, and modern web technologies.**
