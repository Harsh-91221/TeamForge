import { Router } from 'express';
import type { Request, Response } from 'express';
import passport from 'passport';
import { config } from '../config/app.config';
import {
  googleLoginCallback,
  getGoogleFrontendCallbackUrl,
  loginController,
  logOutController,
  registerUserController,
} from '../controllers/auth.controller';

const authRoutes = Router();

authRoutes.post('/register', registerUserController);
authRoutes.post('/login', loginController);
authRoutes.post('/logout', logOutController);

if (
  config.GOOGLE_CLIENT_ID &&
  config.GOOGLE_CLIENT_SECRET &&
  config.GOOGLE_CALLBACK_URL &&
  config.FRONTEND_GOOGLE_CALLBACK_URL
) {
  const failedUrl = getGoogleFrontendCallbackUrl({ status: 'failure' });

  authRoutes.get(
    '/google',
    passport.authenticate('google', {
      scope: ['email', 'profile'],
      session: false,
    })
  );

  authRoutes.get(
    '/google/callback',
    passport.authenticate('google', {
      failureRedirect: failedUrl,
      session: false,
    }),
    googleLoginCallback
  );
} else {
  authRoutes.get('/google', (_req: Request, res: Response): void => {
    res.status(503).json({
      message: 'Google OAuth is not configured',
    });
  });
}

export default authRoutes;

