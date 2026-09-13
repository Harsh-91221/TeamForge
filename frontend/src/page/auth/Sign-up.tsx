import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import Logo from '@/components/logo';
import GoogleOauthButton from '@/components/auth/google-oauth-button';
import { useMutation } from '@tanstack/react-query';
import { registerMutationFn } from '@/lib/api';
import { toast } from '@/hooks/use-toast';
import { Loader } from 'lucide-react';
import { useStore } from '@/store/store';

const SignUp = () => {
  const navigate = useNavigate();
  const { setAccessToekn } = useStore();
  const { mutate, isPending } = useMutation({ mutationFn: registerMutationFn });
  const [searchParams] = useSearchParams();
  const returnUrl = searchParams.get('returnUrl');
  const inviteCode = (() => {
    const direct = searchParams.get('inviteCode');
    if (direct) return direct;
    if (returnUrl) {
      const decoded = decodeURIComponent(returnUrl);
      const match = decoded.match(/\/invite\/workspace\/([^/]+)\/join/);
      return match ? match[1] : undefined;
    }
    return undefined;
  })();
  const formSchema = z.object({
    name: z.string().trim().min(1, {
      message: 'Name is required',
    }),
    email: z.string().trim().email('Invalid email address').min(1, {
      message: 'Workspace name is required',
    }),
    password: z.string().trim().min(8, 'Password must be at least 8 characters')
      .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
      .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
      .regex(/[0-9]/, 'Password must contain at least one number')
      .regex(/[^a-zA-Z0-9]/, 'Password must contain at least one special character'),
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: '',
      password: '',
    },
  });

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    if (isPending) return;
    // If we have an inviteCode from the URL, include it in the registration payload
    // so the backend knows to make the new user join that workspace as a member.
    const payloadWithInvite = inviteCode
      ? { ...values, inviteCode }
      : values;
    mutate(payloadWithInvite, {
      onSuccess: (data) => {
        // Backend now returns access_token + user on registration (auto-login).
        if (data?.access_token) {
          setAccessToekn(data.access_token);
        }
        const decodeUrl = returnUrl ? decodeURIComponent(returnUrl) : null;
        const workspaceId = data?.user?.currentWorkspace?._id;
        if (inviteCode) {
          // When joining via invite, go straight to the invited workspace.
          // The backend already set currentWorkspace to the invited workspace;
          // fall back to the invite page if needed.
          navigate(decodeUrl || (workspaceId ? `/workspace/${workspaceId}` : '/'));
          return;
        }
        navigate(decodeUrl || (workspaceId ? `/workspace/${workspaceId}` : '/'));
      },
      onError: (error) => {
        toast({
          title: 'Error',
          description: error.message,
          variant: 'destructive',
        });
      },
    });
  };

  return (
    <div className="flex min-h-svh flex-col items-center justify-center gap-6 bg-muted p-6 md:p-10">
      <div className="flex w-full max-w-sm flex-col gap-6">
        <Link to="/" className="flex items-center gap-2 self-center font-medium">
          <Logo />
          TeamForge
        </Link>
        <div className="flex flex-col gap-6">
          <Card>
            <CardHeader className="text-center">
              <CardTitle className="text-xl">Create an account</CardTitle>
              <CardDescription>Signup with your Email or Google account</CardDescription>
            </CardHeader>
            <CardContent>
              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)}>
                  <div className="grid gap-6">
                    <div className="flex flex-col gap-4">
                      <GoogleOauthButton label="Signup" />
                    </div>
                    <div className="relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t after:border-border">
                      <span className="relative z-10 bg-background px-2 text-muted-foreground">
                        Or continue with
                      </span>
                    </div>
                    <div className="grid gap-2">
                      <div className="grid gap-2">
                        <FormField
                          control={form.control}
                          name="name"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="dark:text-[#f1f7feb5] text-sm">
                                Name
                              </FormLabel>
                              <FormControl>
                                <Input
                                  placeholder="Joh Doe"
                                  className="!h-[48px]"
                                  {...field}
                                />
                              </FormControl>

                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>
                      <div className="grid gap-2">
                        <FormField
                          control={form.control}
                          name="email"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="dark:text-[#f1f7feb5] text-sm">
                                Email
                              </FormLabel>
                              <FormControl>
                                <Input
                                  placeholder="m@example.com"
                                  className="!h-[48px]"
                                  {...field}
                                />
                              </FormControl>

                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>
                      <div className="grid gap-2">
                        <FormField
                          control={form.control}
                          name="password"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel className="dark:text-[#f1f7feb5] text-sm">
                                Password
                              </FormLabel>
                              <FormControl>
                                <Input type="password" className="!h-[48px]" {...field} />
                              </FormControl>

                              <FormMessage />
                            </FormItem>
                          )}
                        />
                      </div>
                      <Button disabled={isPending} type="submit" className="w-full">
                        {isPending && <Loader className="animate-spin" />}
                        Sign up
                      </Button>
                    </div>
                    <div className="text-center text-sm">
                      Already have an account?{' '}
                      <Link to="/" className="underline underline-offset-4">
                        Sign in
                      </Link>
                    </div>
                  </div>
                </form>
              </Form>
            </CardContent>
          </Card>
          <div className="text-balance text-center text-xs text-muted-foreground [&_a]:underline [&_a]:underline-offset-4 [&_a]:hover:text-primary  ">
            By clicking continue, you agree to our <a href="#">Terms of Service</a> and{' '}
            <a href="#">Privacy Policy</a>.
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignUp;

