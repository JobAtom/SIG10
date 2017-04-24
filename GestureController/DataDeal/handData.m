clear();
data = load('handsSpeed.txt');

[x,y] = size(data);

xaxis = 1: x;

count = 0;
for i = 1:x
    if(data(i)>200)
        count = count+ 1;
    end
end

a = count / x;
x = 0.01:0.1:200;
%z = zeros(500);

z=zeros(1,1999);
yl = log(x);
y = diff(log(x));
for i = 2:1999
    z(i)= y(i)-y(i-1);
end
w = 1:1999;
plot(w , z);
plot(x, yl);

