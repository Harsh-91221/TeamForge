import { baseURL } from '@/lib/base-url';
import { Button } from '../ui/button';

// Extract the invite code from the hash portion of the URL (HashRouter).
// The invite page redirects to "/#/invite/workspace/:code/join" or 
// sign-in/sign-up pages may carry ?inviteCode= in the hash query.
const getInviteCodeFromHash = () => {
  const hash = window.location.hash || '';
  // Remove leading # and split on ?
  const queryStr = hash.split('?')[1] || '';
  const params = new URLSearchParams(queryStr);
  
  // Direct ?inviteCode= in hash query
  const direct = params.get('inviteCode');
  if (direct) return direct;

  // returnUrl in hash query (from InviteUser page)
  const returnUrl = params.get('returnUrl');
  if (returnUrl) {
    try {
      const decoded = decodeURIComponent(returnUrl);
      // Match /invite/workspace/:code/join in the hash path
      const match = decoded.match(/\/invite\/workspace\/([^/]+)\/join/);
      if (match) return match[1];
    } catch {
      // ignore malformed returnUrl
    }
  }
  return undefined;
};

export { getInviteCodeFromHash };

const GoogleOauthButton = (props: { label: string }) => {
  const { label } = props;
  const handleClick = () => {
    const inviteCode = getInviteCodeFromHash();
    const query = inviteCode ? `?inviteCode=${encodeURIComponent(inviteCode)}` : '';
    window.location.href = `${baseURL}/auth/google${query}`;
  };
  return (
    <Button onClick={handleClick} variant="outline" type="button" className="w-full">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path
          d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"
          fill="currentColor"
        />
      </svg>
      {label} with Google
    </Button>
  );
};

export default GoogleOauthButton;

