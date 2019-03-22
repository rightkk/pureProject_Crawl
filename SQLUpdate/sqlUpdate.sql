drop table if exists crawl_communityinfo;

/*==============================================================*/
/* Table: crawl_communityinfo                                   */
/*==============================================================*/
create table crawl_communityinfo
(
   id                   int not null auto_increment,
   communityName        varchar(16),
   streetBlock          varchar(16),
   averagePrice         decimal(6,3),
   propertyFee          decimal(3,2),
   plotRate             decimal(4,2),
   greeningRate         decimal(4,2),
   city                 varchar(8),
   district             varchar(8),
   createTime           datetime,
   primary key (id)
);

alter table crawl_communityinfo comment '小区信息表';

alter table crawl_communityinfo modify column propertyFee decimal(4,2);
alter table crawl_communityinfo MODIFY column averagePrice decimal(10,3)
alter table crawl_communityinfo MODIFY column propertyFee decimal(7,3)
alter table crawl_communityinfo MODIFY column plotRate decimal(6,3)
alter table crawl_communityinfo MODIFY column greeningRate decimal(6,3)


drop table if exists crawl_houseinfo;

/*==============================================================*/
/* Table: crawl_houseinfo                                       */
/*==============================================================*/
create table crawl_houseinfo
(
   id                   int not null auto_increment,
   communityId          int,
   totalPrice           decimal(9,3),
   unitPrice            decimal(6,3),
   houseType            varchar(16),
   decorate             varchar(16),
   legalArea            decimal(4,2),
   useArea              decimal(4,2),
   builtAge             int,
   floor                int,
   rightLimit           int,
   publishDate          date,
   picUrls              text,
   createTime           datetime,
   primary key (id)
);

alter table crawl_houseinfo comment '房屋信息表';

alter table crawl_houseinfo add constraint FK_communityId foreign key (communityId)
      references crawl_communityinfo (id) on delete restrict on update restrict;

alter table crawl_houseinfo modify column floor varchar(16);
alter table crawl_houseinfo MODIFY column unitPrice decimal(10,3)
alter table crawl_houseinfo MODIFY column totalPrice decimal(10,3)
alter table crawl_houseinfo MODIFY column legalArea decimal(8,3)
alter table crawl_houseinfo MODIFY column useArea decimal(8,3)
alter table crawl_houseinfo add title varchar(100) default null;
alter table crawl_houseinfo modify title varchar(100) after communityId;

