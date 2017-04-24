clear();
x = load('trainData01.txt');
y = 1: 139;
B = x(:,2);
minv = min(B);
maxv = max(B);
meanv = mean(B);
figure
plot(y,x(:,1),y,x(:,2),y,x(:,3),y,x(:,4),y,x(:,5),y,x(:,6));
%  figure
%  plot(y, x(:,2));
%  figure
%  plot(y,x(:,3));
%  figure
%  plot(y,x(:,4));
%  figure
%  plot(y,x(:,5));
%  figure
%  plot(y,x(:,6));

