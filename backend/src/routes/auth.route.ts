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
import { getGoogleOAuthState } from '../config/passport.config';

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
    (req: Request, res: Response, next) => {
      // If the user started Google sign-in from an invite link, pass the invite
      // code through a signed OAuth `state` param so it survives the round-trip.
      const inviteCode = (req.query.inviteCode as string) || undefined;
      passport.authenticate('google', {
        scope: ['email', 'profile'],
        state: getGoogleOAuthState(inviteCode),
        session: false,
      })(req, res, next);
    }
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

