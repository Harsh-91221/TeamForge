import { getMembersInWorkspaceQueryFn } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';

const useGetWorkspaceMembers = (workspaceId: string) => {
  const query = useQuery({
    queryKey: ['members', workspaceId],
    queryFn: () => getMembersInWorkspaceQueryFn(workspaceId),
    staleTime: 0,
  });
  return query;
};

export default useGetWorkspaceMembers;

