import { AppBar, Toolbar, Typography, IconButton, Badge, Box } from '@mui/material';
import { Notifications, AccountCircle, Menu as MenuIcon } from '@mui/icons-material';

interface HeaderProps {
  onMenuClick: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <IconButton
          color="inherit"
          edge="start"
          onClick={onMenuClick}
          sx={{ mr: 2, display: { sm: 'none' } }}
        >
          <MenuIcon />
        </IconButton>
        
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          🌾 KrishiMitra
        </Typography>

        <IconButton color="inherit">
          <Badge badgeContent={3} color="error">
            <Notifications />
          </Badge>
        </IconButton>

        <IconButton color="inherit">
          <AccountCircle />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};
