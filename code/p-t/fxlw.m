
function [  ] = trintertime_Count()
%clear;close all;
%clc;
conn = database('sys','root', 'lcjnbnbnb233', 'com.mysql.jdbc.Driver', 'jdbc:mysql://localhost:3306/sys');%���ӵ�mysql
%ping(conn);
%disp('aaaaaaaaaaaaaaaaaaa');
%���ú�ִ��SQL��ѯ���
%queryString = sprintf('SELECT author,time2 FROM zx3000 where time2 between "10-21 9:30" and "11-09 15:00" and comment<>0 group by author,time2');
%queryString = sprintf(['SELECT UserID,Reply_Time FROM qq_0809 where Type = "MsgBoard" group by UserID,Reply_Time'])
%queryString = sprintf(['SELECT QQ1,Reply_Time FROM qq_0809 where QQ1!=QQ2 and Type = "MsgBoard" group by QQ1,Reply_Time'])
queryString = sprintf(['SELECT A.UserID,A.PubTime FROM qq_0809 A,q500 B WHERE A.UserID =B.UserID group by UserID,PubTime'])
%queryString = sprintf('SELECT User_Name,User_Time FROM qq_total_copy group by User_Name,User_Time'); K
%queryString = sprintf('SELECT User_Name,User_Time FROM  qq_total where Group_Name = "IEMS706_��һ" order by User_Name,User_Time'); 
%disp(sprintf('Query string: %s', queryString));
cursor=exec(conn,queryString);%��ִ�����ݿ����ӵ� SQL ���󴴽�����

%��ȡ��ѯ�����Timeseq��Ϊ�������cell��ʽ��
rawdata=fetch(cursor);%ִ�� SQL �������ݵ���MATLAB������
Timeseq=rawdata.Data;
%ͳ�Ƽ��ʱ��

nIndex=1;
m=length(Timeseq)
%if(m>2)
for i=2:m
    ID1=Timeseq(i,1);
    ID2=Timeseq(i-1,1);
    
    if(strcmp(ID1{1},ID2{1}));
        cTime1=Timeseq(i,2);
        t1=cTime1{1};
        cTime2=Timeseq(i-1,2);
        t2=cTime2{1};       
        time1=datenum(t1,'YY-mm-DD HH:MM:SS');
        time2=datenum(t2,'YY-mm-DD HH:MM:SS');
        interTimes(nIndex,1)=(time1-time2)*60*60*24; %#ok<AGROW>#ʱ��1��ȥʱ��2����λ��Ϊ�룩
        nIndex=nIndex+1;    
    end
end

interTimes = floor(interTimes);
%s=tabulate(interTimes(:))

[midP,freq]=lnbin(interTimes,100);
outdata=[midP,freq];



figure
h0=loglog(midP,freq,'o'); 
%xlim(handles.axes1,[30,20000]);
%ylim(handles.axes1,[0.000002,0.009]);
xlabel('��');
ylabel('P(��)');
title("Information posted comment<>0��B3��");
%�����������ָ��,һ��86400��
hold on;

% ������������ߵ�
  %a=polyfit(log(midP(20:55)),log(freq(20:55)),1)
  %disp(a);
  %b=2.71828^a(2)
  %x=10.^1:8.63*10.^4; 
  %y=b*x.^a(1);
  %h1=plot(x,y,'k-','LineWidth',2);
  %hold on;
  %a2=polyfit(log(midP(60:90)),log(freq(60:90)),1)
  %disp(a2);
  %b2=2.71828^a2(2)
  %x2=8.64*10.^4:10.^7; 
  %y2=b2*x2.^a2(1);
  %h2=plot(x2,y2,'k-','LineWidth',2);
  %legend([h0,h1],'����','���ֱ��');
 %������������ߵ�
 %saveas(gca,['G:\paperdata\image\qqGroup' year '_call_' count1 '_' count2 '.fig'],'fig')
%saveas(gcf,['C:\Users\67561\Desktop\���ĸ�������-(' num2str(m) ').fig'],'fig');
%saveas(gcf,['G:\paperdata\image\han\all.fig'],'fig');
%print(gcf,'-djpeg',['C:\Users\67561\Desktop\���ĸ�������-(' num2str(m) ').jpg']);
%close all;
end

